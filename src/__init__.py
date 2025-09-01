"""
富友支付SDK

提供完整的富友支付API封装，包括商户管理、电子协议、支付订单等功能。
"""

from .requests import (
    # 商户管理
    build_mchnt_add_datagram,
    build_machnt_name_check_datagram,

    # 电子协议
    build_elec_contract_generate_datagram,
    build_elec_contract_sign_datagram,
    build_attach_confirm_datagram,

    # 查询接口
    build_chnl_sub_mch_id_query_datagram,
    build_wx_auth_query_datagram,
    build_ali_auth_query_datagram,

    # 支付订单
    build_wx_pre_create_datagram,

    # 工具函数
    xml_to_json,
    post_xml,
    post_json,
    md5_sign,
    rsa_sign,

    # 附件上传
    upload_image,
)

from .oss_upload_file import upload_file
from .bank_code import get_bank_code
from .city_county import get_city_code, get_county_code

__version__ = "0.1.0"
__author__ = "cnjn"
__email__ = "1779895255@qq.com"

__all__ = [
    # 商户管理
    "build_mchnt_add_datagram",
    "build_machnt_name_check_datagram",

    # 电子协议
    "build_elec_contract_generate_datagram",
    "build_elec_contract_sign_datagram",
    "build_attach_confirm_datagram",

    # 查询接口
    "build_chnl_sub_mch_id_query_datagram",
    "build_wx_auth_query_datagram",
    "build_ali_auth_query_datagram",

    # 支付订单
    "build_wx_pre_create_datagram",

    # 工具函数
    "xml_to_json",
    "post_xml",
    "post_json",
    "md5_sign",
    "rsa_sign",

    # 附件上传
    "upload_image",
    "upload_file",

    # 辅助函数
    "get_bank_code",
    "get_city_code",
    "get_county_code",
]
