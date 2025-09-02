import os
from dotenv import load_dotenv

load_dotenv()

from fuiou_sdk.oss_upload_file import upload_file
from fuiou_sdk.requests import (
    build_ali_auth_query_datagram,
    build_chnl_sub_mch_id_query_datagram,
    build_close_order_datagram,
    build_common_query_datagram,
    build_common_refund_datagram,
    build_elec_contract_generate_datagram,
    build_elec_contract_sign_datagram,
    build_attach_confirm_datagram,
    build_get_openid_datagram,
    build_his_trade_query_datagram,
    build_mchnt_add_datagram,
    build_machnt_name_check_datagram,
    build_refund_query_datagram,
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
        "张小红",
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
    datagram = build_elec_contract_generate_datagram(mchnt_cd="0007430FB008217")
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
        mchnt_cd="0007430FB008217",
        verify_no="1756714651117349",
        contract_no="P00000000011906",
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
        mchnt_cd="0007430FB008217",
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
    datagram = build_chnl_sub_mch_id_query_datagram("0002900F0370542", "1")
    response = post_xml(
        "http://www-1.fuiou.com:28090/wmp/wxMchntMng.fuiou?action=chnlSubMchIdQuery",
        datagram,
    )
    print(response)

def test_wx_auth_query():
    """
    测试微信认证查询
    """
    datagram = build_wx_auth_query_datagram("0002900F0370542")
    response = post_xml(
        "http://www-1.fuiou.com:28090/wmp/wxMchntMng.fuiou?action=wxAuthQuery",
        datagram,
    )
    print(response)

def test_ali_auth_query():
    """
    测试支付宝认证查询
    """
    datagram = build_ali_auth_query_datagram("0007430FB008217")
    response = post_xml(
        "http://www-1.fuiou.com:28090/wmp/alipayauth.fuiou?action=alipayAuthQuery",
        datagram,
    )
    print(response)

def test_wx_pre_create():
    """
    测试预订单创建
    """
    os.environ["WX_APPID"] = "wxfa089da95020ba1a"
    datagram = build_wx_pre_create_datagram("0002900F0313432", "SDK演示商品", "1", "127.0.0.1", "JSAPI", "ooIeqs9yLs5l059_0kG91ToqCYSs")
    response = post_xml(
        "https://fundwx.fuiou.com/wxPreCreate",
        datagram,
    )
    print(response)

def test_xml_to_json():
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

def test_oss_upload_file():
    url = upload_file("main.py", "main.py")
    print(url)

def test_rsa_sign():
    sign = rsa_sign("""<?xml version="1.0" encoding="GBK" standalone="yes"?>
<xml>
    <reserved_fy_term_sn></reserved_fy_term_sn>
    <reserved_device_info></reserved_device_info>
    <term_id>12345678</term_id>
    <random_str>d0194c1024f180065d2434fa8b6a2f82</random_str>
    <reserved_limit_pay></reserved_limit_pay>
    <reserved_sub_appid></reserved_sub_appid>
    <ins_cd>08A9999999</ins_cd>
    <reserved_fy_term_type></reserved_fy_term_type>
    <version>1</version>
    <addn_inf></addn_inf>
    <mchnt_cd>0002900F0370542</mchnt_cd>
    <reserved_expire_minute></reserved_expire_minute>
    <term_ip>127.0.0.1</term_ip>
    <notify_url>https://mail.qq.com/cgi-bin/frame_html?sid=pEYG5nBgQiNVqANe&amp;r=4a6c47ad7d279a80630dec073cda96e2</notify_url>
    <order_amt>1</order_amt>
    <goods_des>卡盟测试</goods_des>
    <reserved_hb_fq_seller_percent></reserved_hb_fq_seller_percent>
    <curr_type></curr_type>
    <txn_begin_ts>20201201151802</txn_begin_ts>
    <sign>
        DXNr4zU78EF7R/dknRsVYNWwJ29M6l4YMZrOjqZbNYW9m90yq/n76lO4sS4r8rls0cEz6aRppfLaMkcoyyEqOCRyRnZoCdbi/EW8toU8UhIm+J0J+I9lFe+IqD6fOQ73c6iNzQ0Bvt9nTYvU2WvbKH4xIDntA0Sw7prNGJiq6iI=
    </sign>
    <goods_tag></goods_tag>
    <goods_detail>asasda</goods_detail>
    <reserved_fy_term_id></reserved_fy_term_id>
    <reserved_hb_fq_num></reserved_hb_fq_num>
    <mchnt_order_no>202012011518020724446</mchnt_order_no>
    <order_type>WECHAT</order_type>
</xml>""")
    print(sign)    

def test_common_query():
    """
    测试订单查询
    """
    datagram = build_common_query_datagram("0002900F0313432", "202012011518020724446", "WECHAT")
    response = post_xml(
        "https://fundwx.fuiou.com/commonQuery", datagram)
    print(response)

def test_common_refund():
    """
    测试订单退款
    """
    datagram = build_common_refund_datagram("0002900F0313432", "202012011518020724446", "WECHAT", "202012011518020724446_refund", 1, 1)
    response = post_xml(
        "https://fundwx.fuiou.com/commonRefund", datagram)
    print(response)

def test_his_trade_query():
    """
    测试历史交易查询
    """
    datagram = build_his_trade_query_datagram("0002900F0313432", "202012011518020724446", "WECHAT", "20201201")
    response = post_xml(
        "https://fundwx.fuiou.com/hisTradeQuery", datagram)
    print(response)

def test_get_openid():
    """
    测试获取OpenID
    """
    datagram = build_get_openid_datagram("0002900F0313432", "http://lo.yesmola.net/api/v2/api/wechat/openid_callback?extra=")
    url = f"http://fundwx.fuiou.com/oauth2/getOpenid?{datagram}"
    print(url)

def test_refund_query():
    """
    测试退款查询
    """
    datagram = build_refund_query_datagram("0002900F0313432", "202012011518020724446_refund")
    response = post_xml(
        "https://fundwx.fuiou.com/refundQuery", datagram)
    print(response)

def test_close_order():
    """
    测试关闭订单
    """
    datagram = build_close_order_datagram("0002900F0313432", "202012011518020724446", "WECHAT", "wxfa089da95020ba1a")
    response = post_xml(
        "https://fundwx.fuiou.com/closeorder", datagram)
    print(response)

if __name__ == "__main__":
    # test_mchnt_add()  # {'trace_no': '', 'mchnt_name': '', 'fy_mchnt_cd': '0007430FB008217', 'ret_msg': '操作成功', 'wxapp_mchnt_cd': '', 'is_effective_acnt': '', 'acnt_upd_no': '', 'ret_code': '0000', 'wx_mchnt_cd': '', 'auto_buy_cd': '', 'auto_buy_msg': '', 'wechat_mchnt_cd': '', 'acnt_upd_st': '', 'acnt_upd_msg': '', 'acnt_upd_ts': ''}
    # test_mchnt_name_check()
    # test_elec_contract_generate()  # {"acnt_no":"6222022507002349308","bank_nm":"中国工商银行云南红河分行泸西城区支行","contract_content":"","contract_no":"P00000000011906","expire_ts":"20250901 16:47:31","mchnt_cd":"0007430FB008217","mchnt_name":"张小红","ret_code":"0000","ret_msg":"操作成功","sign":"c296333c9236cd6d63816a52fe5fad07","sign_url":"https://mchntapi.fuioupay.com/wxMchntMng.fuiou?action=elecContract&sign=C877CA93DEE9EA22CD65F40E464A18FC","trace_no":"250901161729","verify_no":"1756714651117349"}
    # test_elec_contract_sign()  # {"acnt_no":"","bank_nm":"","contract_content":"","contract_no":"","expire_ts":"","mchnt_cd":"","mchnt_name":"","ret_code":"0000","ret_msg":"操作成功","sign":"6b6e211a64f3b49992f29bb522e2af74","sign_url":"","trace_no":"","verify_no":""}
    # code = upload_image(
    #     "0007430FB008217",
    #     "src/image1.jpg",
    #     "src/image2.jpg",
    #     "src/image3.jpg",
    #     "src/image4.jpg",
    #     "src/image5.jpg",
    # )
    # print(code)  # 226 Transfer complete
    # test_attach_confirm() # {"contact_url":"","ret_code":"0000","ret_msg":"操作成功","sign":"edfcec1127976e1590f0fe36e70ce343","trace_no":"250901163301"}
    # test_chnl_sub_mch_id_query()
    # 查询微信渠道号：{'trace_no': '250901163335', 'mchnt_cd': '0007430FB008217', 'sub_mch_id': '805611561', 'result_code': 'SUCCESS', 'result_msg': 'OK', 'link_mchnt_cd': '', 'return_code': 'SUCCESS', 'return_msg': '', 'ali_link_mchnt_cd': '', 'wx_channel_no': '24006513'}
    # 查询支付宝渠道: {'trace_no': '250901163525', 'mchnt_cd': '0007430FB008217', 'sub_mch_id': '2088870984475260', 'result_code': 'SUCCESS', 'result_msg': 'OK', 'link_mchnt_cd': '', 'return_code': 'SUCCESS', 'return_msg': '', 'ali_link_mchnt_cd': '', 'wx_channel_no': ''}
    # test_wx_auth_query()  # {'trace_no': '250901163713', 'return_code': 'SUCCESS', 'return_msg': '', 'mchnt_cd': '0007430FB008217', 'result_msg': 'OK', 'result_code': 'SUCCESS', 'channel_infos': [{'channel_name': '普通1', 'sub_mch_id': '805611561', 'authorize_state': '1', 'reject_msgs': '', 'qr_code': '', 'curr_channel': '1'}]}
    # test_ali_auth_query()  # {'trace_no': '250901163939', 'return_code': 'SUCCESS', 'return_msg': '', 'mchnt_cd': '0007430FB008217', 'result_msg': 'OK', 'result_code': 'SUCCESS', 'channel_infos': [{'channel_name': '银联普通', 'sub_mch_id': '2088870984475260', 'authorize_state': '1', 'reject_msgs': '', 'qr_code': '', 'curr_channel': '1'}]}
    # test_get_openid()  # {"openid":"ooIeqs9yLs5l059_0kG91ToqCYSs","appid":"wxfa089da95020ba1a"}
    # test_wx_pre_create()
    # test_common_query()
    # test_common_refund()
    # test_refund_query()
    # test_his_trade_query()
    test_close_order()
