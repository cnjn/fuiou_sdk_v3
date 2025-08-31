import os
from dotenv import load_dotenv

load_dotenv()

from src.oss_upload_file import upload_file
from src.requests import (
    build_ali_auth_query_datagram,
    build_chnl_sub_mch_id_query_datagram,
    build_elec_contract_generate_datagram,
    build_elec_contract_sign_datagram,
    build_attach_confirm_datagram,
    build_mchnt_add_datagram,
    build_machnt_name_check_datagram,
    build_wx_auth_query_datagram,
    build_wx_pre_create_datagram,
    post_json,
    post_xml,
    rsa_sign,
    upload_image,
    xml_to_json,
)


def test_mchnt_add():
    """
    测试商户添加
    """
    datagram = build_mchnt_add_datagram(
        "张春绿",
        "兄弟动漫",
        "53252719900116081X",
        "云南省红河哈尼族彝族自治州泸西县三塘乡布德龙上寨村",
        "20230403",
        "20430403",
        "18787316994",
        "云南省红河哈尼族彝族自治州泸西县中枢镇小村86号",
        "红河哈尼族彝族自治州",
        "泸西县",
        "中国工商银行云南红河分行泸西城区支行",
        "6222022507002349308",
        "13887576111",
    )
    response = post_xml(
        "http://www-1.fuiou.com:28090/wmp/wxMchntMng.fuiou?action=wxMchntAdd", datagram
    )
    print(response)

def test_mchnt_name_check():
    """
    测试商户名称判重
    """
    datagram = build_machnt_name_check_datagram("商户 张春绿")
    response = post_xml(
        "http://www-1.fuiou.com:28090/wmp/wxMchntMng.fuiou?action=wxMchntNameCheck",
        datagram,
    )
    print(response)

def test_elec_contract_generate():
    """
    测试电子协议生成
    """
    datagram = build_elec_contract_generate_datagram("0007430FB008211")
    response = post_json(
        "http://www-1.fuiou.com:28090/wmp/wxMchntMng.fuiou?action=elecContractGenerate",
        datagram,
    )
    print(response)

def test_elec_contract_sign():
    """
    测试电子协议签署
    """
    datagram = build_elec_contract_sign_datagram(
        mchnt_cd="0002900F8005076",
        verify_no="1568687914072173",
        contract_no="P00000000003030",
    )
    response = post_json(
        "http://www-1.fuiou.com:28090/wmp/wxMchntMng.fuiou?action=elecContractSign",
        datagram,
    )
    print(response)

def test_attach_confirm():
    """
    测试附件提交完成
    """
    datagram = build_attach_confirm_datagram(
        mchnt_cd="0005410F0659988",
    )
    response = post_json(
        "http://www-1.fuiou.com:28090/wmp/wxMchntMng.fuiou?action=attachConfirm",
        datagram,
    )
    print(response)

def test_chnl_sub_mch_id_query():
    """
    测试渠道子商户号查询
    """
    datagram = build_chnl_sub_mch_id_query_datagram("0005410F0659988", "1")
    response = post_xml(
        "http://www-1.fuiou.com:28090/wmp/wxMchntMng.fuiou?action=chnlSubMchIdQuery",
        datagram,
    )
    print(response)

def test_wx_auth_query():
    """
    测试微信认证查询
    """
    datagram = build_wx_auth_query_datagram("0005410F0659988")
    response = post_xml(
        "http://www-1.fuiou.com:28090/wmp/wxMchntMng.fuiou?action=wxAuthQuery",
        datagram,
    )
    print(response)

def test_ali_auth_query():
    """
    测试支付宝认证查询
    """
    datagram = build_ali_auth_query_datagram("0005410F0659988")
    response = post_xml(
        "http://www-1.fuiou.com:28090/wmp/alipayauth.fuiou?action=alipayAuthQuery",
        datagram,
    )
    print(response)

def test_wx_pre_create():
    """
    测试预订单创建
    """
    datagram = build_wx_pre_create_datagram(os.getenv("FUIOU_MCHNT_ID"), "SDK演示商品", "1", "127.0.0.1", "JSAPI", "o0UxH5M6tzzPpC39jzR-JMsNjX80")
    response = post_xml(
        "https://fundwx.fuiou.com/wxPreCreate",
        datagram,
    )
    print(response)

if __name__ == "__main__":
    test_mchnt_add()
    test_mchnt_name_check()
    test_elec_contract_generate()
    test_elec_contract_sign()
    test_attach_confirm()
    test_chnl_sub_mch_id_query()
    test_wx_auth_query()
    test_ali_auth_query()
    s = xml_to_json("""<?xml version="1.0" encoding="utf-8"?>
<xml>
  <trace_no></trace_no>
  <return_code>SUCCESS</return_code>
  <return_msg/>
  <mchnt_cd/>
  <result_msg>OK</result_msg>
  <result_code>SUCCESS</result_code>
  <channel_infos>
    <channel_info>
      <channel_name>银联普通</channel_name>
      <sub_mch_id>123456789</sub_mch_id>
      <authorize_state>4</authorize_state>
      <reject_msgs/>
      <qr_code/>
      <curr_channel>1</curr_channel>
    </channel_info>
  </channel_infos>
</xml>""")
    print(s)
#     url = upload_file("main.py", "main.py")
#     print(url)

#     # upload_image(
#     #     "0005410F0659988",
#     #     "src/image.jpg",
#     #     "src/image.jpg",
#     #     "src/image.jpg",
#     #     "src/image.jpg",
#     #     "src/image.jpg",
#     # )

#     sign = rsa_sign("""<?xml version="1.0" encoding="GBK" standalone="yes"?>
# <xml>
#     <reserved_fy_term_sn></reserved_fy_term_sn>
#     <reserved_device_info></reserved_device_info>
#     <term_id>12345678</term_id>
#     <random_str>d0194c1024f180065d2434fa8b6a2f82</random_str>
#     <reserved_limit_pay></reserved_limit_pay>
#     <reserved_sub_appid></reserved_sub_appid>
#     <ins_cd>08A9999999</ins_cd>
#     <reserved_fy_term_type></reserved_fy_term_type>
#     <version>1</version>
#     <addn_inf></addn_inf>
#     <mchnt_cd>0002900F0370542</mchnt_cd>
#     <reserved_expire_minute></reserved_expire_minute>
#     <term_ip>127.0.0.1</term_ip>
#     <notify_url>https://mail.qq.com/cgi-bin/frame_html?sid=pEYG5nBgQiNVqANe&amp;r=4a6c47ad7d279a80630dec073cda96e2</notify_url>
#     <order_amt>1</order_amt>
#     <goods_des>卡盟测试</goods_des>
#     <reserved_hb_fq_seller_percent></reserved_hb_fq_seller_percent>
#     <curr_type></curr_type>
#     <txn_begin_ts>20201201151802</txn_begin_ts>
#     <sign>
#         DXNr4zU78EF7R/dknRsVYNWwJ29M6l4YMZrOjqZbNYW9m90yq/n76lO4sS4r8rls0cEz6aRppfLaMkcoyyEqOCRyRnZoCdbi/EW8toU8UhIm+J0J+I9lFe+IqD6fOQ73c6iNzQ0Bvt9nTYvU2WvbKH4xIDntA0Sw7prNGJiq6iI=
#     </sign>
#     <goods_tag></goods_tag>
#     <goods_detail>asasda</goods_detail>
#     <reserved_fy_term_id></reserved_fy_term_id>
#     <reserved_hb_fq_num></reserved_hb_fq_num>
#     <mchnt_order_no>202012011518020724446</mchnt_order_no>
#     <order_type>WECHAT</order_type>
# </xml>""")
#     print(sign)
    test_wx_pre_create()