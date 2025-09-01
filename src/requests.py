DATAGRAMS_DIR = __file__.replace("requests.py", "/datagrams/requests")

import hashlib
import json
import os
from datetime import datetime
import random
import string
import xml.etree.ElementTree as ET
from .city_county import get_city_code, get_county_code
from .bank_code import get_bank_code
import requests
import urllib.parse
from typing import Literal
import zipfile
import tempfile
import ftplib
import os
import base64
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
from Crypto.Signature import PKCS1_v1_5


def xml_to_json(xml: str):
    """
    将XML转换为JSON
    """
    try:
        # 移除XML声明（如果存在）
        if xml.startswith('<?xml'):
            xml = xml.split('?>', 1)[1]
        
        # 解析XML
        root = ET.fromstring(xml)

        def parse_element(element: ET.Element):
            children = list(element)
            # 叶子节点：返回文本（去除空白；为空返回空字符串）
            if not children:
                if element.text is None:
                    return ""
                text = element.text.strip()
                return text if text else ""

            # 非叶子：解析子节点
            grouped: dict[str, object] = {}
            for child in children:
                value = parse_element(child)
                if child.tag in grouped:
                    # 已存在同名键：聚合为列表
                    existing = grouped[child.tag]
                    if isinstance(existing, list):
                        existing.append(value)
                    else:
                        grouped[child.tag] = [existing, value]
                else:
                    grouped[child.tag] = value

            # 如果所有子节点标签相同，直接返回其列表（或单个元素形成的列表）
            child_tags = [c.tag for c in children]
            if len(set(child_tags)) == 1:
                only_tag = child_tags[0]
                only_value = grouped[only_tag]
                return only_value if isinstance(only_value, list) else [only_value]

            return grouped

        # 根节点下一层展开为字典
        result: dict[str, object] = {}
        for elem in root:
            result[elem.tag] = parse_element(elem)

        return result
    except ET.ParseError as e:
        print(e)
        # 如果XML解析失败，返回原始字符串
        return xml

def md5_sign(xml_str: str):
    """
    对XML报文进行MD5签名
    只有传值的字段参与签名，空字段不参与签名
    """
    # 解析XML
    root = ET.fromstring(xml_str)

    # 收集所有有值的字段
    sign_fields = []
    for elem in root:
        if elem.text and elem.text.strip():  # 只有非空字段参与签名
            sign_fields.append(f"{elem.tag}={elem.text}")

    # 按字段名排序
    sign_fields.sort()

    # 拼接签名字符串
    sign_str = "&".join(sign_fields)

    # 添加密钥
    key = os.getenv("FUIOU_MD5_KEY", "")
    sign_str += f"&key={key}"

    # 计算MD5签名
    md5_hash = hashlib.md5(sign_str.encode("GBK")).hexdigest()

    return md5_hash

def rsa_sign(xml_str: str):
    """
    对XML报文进行RSA签名
    sign字段不参与签名
    reserved开头的字段不参与签名
    其他字段全部参与签名
    """
    # 解析XML
    root = ET.fromstring(xml_str)

    # 收集所有有值的字段
    sign_fields = []
    for elem in root:
        if not (elem.tag == 'sign' or elem.tag.startswith('reserved')):
            sign_fields.append(f"{elem.tag}={elem.text if elem.text else ''}")

    # 按字段名排序
    sign_fields.sort()

    # 拼接签名字符串
    sign_str = "&".join(sign_fields)

    # 导入私钥
    key = RSA.import_key("""-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAJgAzD8fEvBHQTyxUEeK963mjziM
WG7nxpi+pDMdtWiakc6xVhhbaipLaHo4wVI92A2wr3ptGQ1/YsASEHm3m2wGOpT2vrb2Ln/S7lz1
ShjTKaT8U6rKgCdpQNHUuLhBQlpJer2mcYEzG/nGzcyalOCgXC/6CySiJCWJmPyR45bJAgMBAAEC
gYBHFfBvAKBBwIEQ2jeaDbKBIFcQcgoVa81jt5xgz178WXUg/awu3emLeBKXPh2i0YtN87hM/+J8
fnt3KbuMwMItCsTD72XFXLM4FgzJ4555CUCXBf5/tcKpS2xT8qV8QDr8oLKA18sQxWp8BMPrNp0e
pmwun/gwgxoyQrJUB5YgZQJBAOiVXHiTnc3KwvIkdOEPmlfePFnkD4zzcv2UwTlHWgCyM/L8SCAF
clXmSiJfKSZZS7o0kIeJJ6xe3Mf4/HSlhdMCQQCnTow+TnlEhDTPtWa+TUgzOys83Q/VLikqKmDz
kWJ7I12+WX6AbxxEHLD+THn0JGrlvzTEIZyCe0sjQy4LzQNzAkEAr2SjfVJkuGJlrNENSwPHMugm
vusbRwH3/38ET7udBdVdE6poga1Z0al+0njMwVypnNwy+eLWhkhrWmpLh3OjfQJAI3BV8JS6xzKh
5SVtn/3Kv19XJ0tEIUnn2lCjvLQdAixZnQpj61ydxie1rggRBQ/5vLSlvq3H8zOelNeUF1fT1QJA
DNo+tkHVXLY9H2kdWFoYTvuLexHAgrsnHxONOlSA5hcVLd1B3p9utOt3QeDf6x2i1lqhTH2w8gzj
vsnx13tWqg==
-----END PRIVATE KEY-----""")
    key = RSA.import_key(os.getenv("PRIVATE_KEY", ""))
    signer = PKCS1_v1_5.new(key)
    
    # 使用GBK编码
    data_bytes = sign_str.encode('gbk')
    
    # MD5哈希
    hash_obj = MD5.new(data_bytes)
    
    # RSA签名
    signature = signer.sign(hash_obj)
    
    # Base64编码
    return base64.b64encode(signature).decode('utf-8')

def post_xml(url: str, datagram: str):
    """
    发送POST请求
    """
    # 对XML报文进行URL编码
    encoded_req = urllib.parse.quote_plus(datagram, encoding="GBK")

    # 发送POST请求
    response = requests.post(
        url,
        data={"req": encoded_req},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    response = urllib.parse.unquote_plus(response.text, encoding="GBK")
    return xml_to_json(response)

def post_json(url: str, datagram: dict):
    """
    发送POST请求
    """
    sign_field = []

    for key, value in datagram.items():
        if value:
            sign_field.append(f"{key}={value}")

    sign_field.sort()
    sign_field = "&".join(sign_field)
    sign_field += f"&key={os.getenv('FUIOU_MD5_KEY', '')}"
    sign = hashlib.md5(sign_field.encode("GBK")).hexdigest()
    datagram["sign"] = sign

    response = requests.post(url, data={"req": json.dumps(datagram)})
    return response.text

def build_mchnt_add_datagram(
    mchnt_name: str,
    mchnt_shortname: str,
    id_card: str,
    id_addr: str,
    start_dt: str,
    expire_dt: str,
    contact_mobile: str,
    addr: str,
    city: str,
    county: str,
    bank: str,
    account: str,
    account_mobile: str,
):
    """
    mchnt_name: 商户姓名
    mchnt_shortname: 商户简称
    id_card: 身份证号
    id_addr: 身份证地址
    start_dt: 身份证开始日(YYYYMMDD)
    expire_dt: 身份证到期日(YYYYMMDD)
    contact_mobile: 联系手机号
    addr: 联系地址
    city: 城市
    county: 区县
    bank: 开户行
    account: 账户
    account_name: 户名
    account_mobile: 银行预留手机号
    """

    # 解析模板
    template = f"{DATAGRAMS_DIR}/wxMchntAdd.xml"
    tree = ET.parse(template)
    root = tree.getroot()

    # 生成/读取通用参数
    trace_no = datetime.now().strftime("%y%m%d%H%M%S")  # 12位
    ins_cd = os.getenv("FUIOU_INS_CD", "")  # 机构号
    sub_ins_cd = os.getenv("FUIOU_SUB_INS_CD", "")  # 二级代理机构号(可选)

    # 代码/联行号映射
    city_cd = get_city_code(city)
    county_cd = get_county_code(county)
    inter_bank_no = get_bank_code(bank)

    assert city_cd != "", f"城市代码为空: {city}"
    assert county_cd != "", f"区县代码为空: {county}"
    assert inter_bank_no != "", f"联行号为空: {bank}"

    # 写入模板
    def set_text(tag: str, val: str):
        el = root.find(tag)
        if el is not None:
            el.text = val

    set_text("trace_no", trace_no)
    set_text("ins_cd", ins_cd)
    set_text("sub_ins_cd", sub_ins_cd)

    set_text("mchnt_name", f"商户 {mchnt_name}")
    set_text("mchnt_shortname", mchnt_shortname)
    # real_name 保持空
    # license_type 保持 A

    set_text("license_no", id_card)
    set_text("license_expire_dt", expire_dt)

    set_text("certif_id", id_card)
    set_text("certif_id_expire_dt", expire_dt)

    set_text("contact_person", mchnt_name)
    set_text("contact_phone", contact_mobile)
    set_text("contact_addr", addr)
    set_text("contact_mobile", contact_mobile)
    # contact_email 保持空

    # 经营范围 business 模板默认为 56，如需可调整
    set_text("city_cd", city_cd)
    set_text("county_cd", county_cd)

    # 入账信息（模板 acnt_type=2 对私；bank_type 保持空；）
    set_text("inter_bank_no", inter_bank_no)
    set_text("iss_bank_nm", bank)
    set_text("acnt_nm", mchnt_name)
    set_text("acnt_no", account)

    # 清算类型 settle_tp 模板默认 1（T1自动）
    set_text("artif_nm", mchnt_name)  # 无单独法人名参数时按姓名填
    # acnt_artif_flag=1 法人入账；acnt_certif_tp=0 身份证
    set_text("acnt_certif_id", id_card)
    set_text("acnt_certif_expire_dt", expire_dt)
    set_text("acnt_contact_mobile", account_mobile)

    # 可选/附加字段
    set_text("contact_cert_no", id_card)
    set_text("license_start_dt", start_dt)
    set_text("lic_regis_addr", id_addr)
    set_text("card_start_dt", start_dt)
    # set_text("certif_phone", contact_mobile)
    set_text("certif_addr", id_addr)

    # 其它开关按模板默认值：
    # wx_flag=1, ali_flag=1, wx_set_cd=M0000, ali_set_cd=M0000, wx_busi_flag=0, th_flag=0

    # 生成XML（保留GBK声明；禁止空字符串折叠为自闭合标签）
    xml_str = ET.tostring(root, encoding="GBK", short_empty_elements=False).decode("GBK")

    # 对XML报文进行MD5签名
    sign = md5_sign(xml_str)
    xml_str = xml_str.replace("<sign></sign>", f"<sign>{sign}</sign>")

    return xml_str


def build_machnt_name_check_datagram(mchnt_name: str):
    """
    根据模板 wxMchntNameCheck.xml 生成商户名称判重报文
    mchnt_name: 商户姓名
    """

    # 解析模板
    template = f"{DATAGRAMS_DIR}/wxMchntNameCheck.xml"
    tree = ET.parse(template)
    root = tree.getroot()

    # 通用参数
    trace_no = datetime.now().strftime("%y%m%d%H%M%S")  # 12位
    ins_cd = os.getenv("FUIOU_INS_CD", "")  # 机构号

    # 写入模板
    def set_text(tag: str, val: str):
        el = root.find(tag)
        if el is not None:
            el.text = val

    set_text("trace_no", trace_no)
    set_text("ins_cd", ins_cd)
    set_text("mchnt_name", mchnt_name)

    # 生成XML
    xml_str = ET.tostring(root, encoding="GBK", short_empty_elements=False).decode("GBK")

    # 签名
    sign = md5_sign(xml_str)
    xml_str = xml_str.replace("<sign></sign>", f"<sign>{sign}</sign>")

    return xml_str


def build_elec_contract_generate_datagram(mchnt_cd: str):
    """
    电子协议生成
    """
    return {
        "trace_no": datetime.now().strftime("%y%m%d%H%M%S"),
        "ins_cd": os.getenv("FUIOU_INS_CD", ""),
        "mchnt_cd": mchnt_cd,
    }


def build_elec_contract_sign_datagram(
    mchnt_cd: str,
    verify_no: str,
    contract_no: str,
):
    """
    电子协议签署（elecContractSign）
    mchnt_cd: 商户编码
    verify_no: 验证码
    contract_no: 协议编号
    """

    return {
        "trace_no": datetime.now().strftime("%y%m%d%H%M%S"),
        "ins_cd": os.getenv("FUIOU_INS_CD", ""),
        "mchnt_cd": mchnt_cd,
        "verify_no": verify_no,
        "contract_no": contract_no,
    }


def build_attach_confirm_datagram(mchnt_cd: str):
    """
    附件提交完成（attachConfirm）
    ins_cd: 机构号
    trace_no: 流水号
    mchnt_cd: 商户号
    """

    return {
        "ins_cd": os.getenv("FUIOU_INS_CD", ""),
        "trace_no": datetime.now().strftime("%y%m%d%H%M%S"),
        "mchnt_cd": mchnt_cd,
    }

def build_chnl_sub_mch_id_query_datagram(mchnt_cd: str, mchnt_tp: Literal["1", "2"]):
    """
    渠道子商户号查询
    mchnt_cd: 商户号
    mchnt_tp: 1 代表微信， 2 代表支付宝
    """
    template = f"{DATAGRAMS_DIR}/chnlSubMchIdQuery.xml"
    tree = ET.parse(template)
    root = tree.getroot()

    def set_text(tag: str, val: str):
        el = root.find(tag)
        if el is not None:
            el.text = val

    set_text("trace_no", datetime.now().strftime("%y%m%d%H%M%S"))
    set_text("ins_cd", os.getenv("FUIOU_INS_CD", ""))
    set_text("mchnt_cd", mchnt_cd)
    set_text("mchnt_tp", mchnt_tp)

    xml_str = ET.tostring(root, encoding="GBK", short_empty_elements=False).decode("GBK")
    sign = md5_sign(xml_str)
    xml_str = xml_str.replace("<sign></sign>", f"<sign>{sign}</sign>")
    return xml_str

def build_wx_auth_query_datagram(mchnt_cd: str):
    """
    微信认证查询
    """
    # 解析模板
    template = f"{DATAGRAMS_DIR}/wxAuthQuery.xml"
    tree = ET.parse(template)
    root = tree.getroot()

    # 通用参数
    trace_no = datetime.now().strftime("%y%m%d%H%M%S")  # 12位
    ins_cd = os.getenv("FUIOU_INS_CD", "")  # 机构号

    # 写入模板
    def set_text(tag: str, val: str):
        el = root.find(tag)
        if el is not None:
            el.text = val

    set_text("trace_no", trace_no)
    set_text("ins_cd", ins_cd)
    set_text("mchnt_cd", mchnt_cd)

    # 生成XML
    xml_str = ET.tostring(root, encoding="GBK", short_empty_elements=False).decode("GBK")

    # 签名
    sign = md5_sign(xml_str)
    xml_str = xml_str.replace("<sign></sign>", f"<sign>{sign}</sign>")

    return xml_str

def build_ali_auth_query_datagram(mchnt_cd: str):
    """
    支付宝认证查询
    """
    return build_wx_auth_query_datagram(mchnt_cd)
    
def upload_image(
    mchnt_cd: str,
    id_card_front_image: str,
    id_card_back_image: str,
    inner_image: str,  # 门脸图片, 就是内设照片
    outer_image: str,  # 门头照片
    bank_card_front_image: str,
):

    def encode(file_name: str):
        return urllib.parse.quote_plus(file_name, safe="", encoding="GBK").replace("%", "").lower()
    
    # 编码后的文件名
    encoded_names = {
        id_card_front_image: encode("法人身份证明正面.jpg"),
        id_card_back_image: encode("法人身份证明反面.jpg"),
        inner_image: encode("门脸照片.jpg"),
        outer_image: encode("门头照片.jpg"),
        bank_card_front_image: encode("银行卡正面.jpg")
    }
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, f"{mchnt_cd}.zip")
        
        # 创建压缩包
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for local_path, encoded_name in encoded_names.items():
                if os.path.exists(local_path):
                    zipf.write(local_path, encoded_name)
        
        # 通过FTP上传
        with ftplib.FTP() as ftp:
            ftp.connect("ftp-1.fuiou.com", 9021)
            ftp.login("FTP999999", "8A4GL0qVNd4RWhtK")
            
            with open(zip_path, 'rb') as file:
                code = ftp.storbinary(f'STOR /{mchnt_cd}.zip', file)

    # TODO: 把文件上传到OSS，返回OSS的URL

    return code

def build_wx_pre_create_datagram(
    mchnt_cd: str,
    goods_des: str,
    # mchnt_order_no: str,
    order_amt: str,
    term_ip: str,
    trade_type: Literal["JSAPI", "FWC"],
    openid: str,
):
    """
    创建订单
    mchnt_cd: 商户号
    goods_des: 商品描述
    ~~mchnt_order_no: 内部订单号~~
    order_amt: 订单金额（分）
    term_ip: 终端IP
    trade_type: 交易类型, JSAPI 代表公众号, FWC 代表微信小程序
    openid: 用户OpenID
    """
    # 解析模板
    template = f"{DATAGRAMS_DIR}/wxPreCreate.xml" 
    tree = ET.parse(template)
    root = tree.getroot()

    # 通用参数
    trace_no = datetime.now().strftime("%y%m%d%H%M%S")  # 12位
    ins_cd = os.getenv("FUIOU_INS_CD", "")  # 机构号

    # 写入模板
    def set_text(tag: str, val: str):
        el = root.find(tag)
        if el is not None:
            el.text = val

    # set_text("trace_no", trace_no)
    set_text("ins_cd", ins_cd)
    set_text("mchnt_cd", mchnt_cd)
    set_text("random_str", ''.join(random.choices(string.ascii_letters + string.digits, k=32)))
    set_text("goods_des", goods_des)
    set_text("mchnt_order_no", datetime.now().strftime("%y%m%d%H%M%S"))
    set_text("order_amt", order_amt)
    set_text("term_ip", term_ip)
    set_text("txn_begin_ts", datetime.now().strftime(r"%Y%m%d%H%M%S"))
    set_text("notify_url", os.getenv("FUIOU_NOTIFY_URL", ""))
    set_text("trade_type", trade_type)
    set_text("sub_openid", openid)
    set_text("sub_appid", os.getenv("WX_APPID", "") if trade_type == "JSAPI" else os.getenv("ALI_APPID", ""))

    # 生成XML
    xml_str = ET.tostring(root, encoding="GBK", short_empty_elements=False).decode("GBK")

    # 签名
    sign = rsa_sign(xml_str)
    xml_str = xml_str.replace("<sign></sign>", f"<sign>{sign}</sign>")

    return xml_str