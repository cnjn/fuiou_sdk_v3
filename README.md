# 富友支付SDK (fuiou-sdk)

[![PyPI version](https://badge.fury.io/py/fuiou-sdk.svg)](https://pypi.org/project/fuiou-sdk/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

富友支付Python SDK，支持商户管理、电子协议、支付订单等完整功能。

## 功能特性

- ✅ 商户管理 (添加、名称检查)
- ✅ 电子协议生成和签署
- ✅ 附件上传 (FTP + OSS)
- ✅ 渠道子商户号查询
- ✅ 微信/支付宝认证查询
- ✅ 预订单创建 (JSAPI、小程序)
- ✅ XML/JSON 数据转换
- ✅ MD5/RSA 签名算法
- ✅ 省市区代码自动映射
- ✅ 银行联行号自动查询

## 安装

```bash
pip install fuiou-sdk
# 或使用 uv
uv add fuiou-sdk
```

## 快速开始

```python
import os
from fuiou_sdk import (
    build_mchnt_add_datagram,
    build_wx_pre_create_datagram,
    post_xml,
    post_json
)

# 设置环境变量
os.environ['FUIOU_INS_CD'] = 'your_ins_cd'
os.environ['FUIOU_MD5_KEY'] = 'your_md5_key'
os.environ['FUIOU_MCHNT_ID'] = 'your_mchnt_id'

# 创建商户
datagram = build_mchnt_add_datagram(
    mchnt_name="张三",
    mchnt_shortname="张三商店",
    id_card="123456789012345678",
    id_addr="北京市朝阳区",
    start_dt="20200101",
    expire_dt="20300101",
    contact_mobile="13800138000",
    addr="北京市朝阳区某某街道",
    city="北京市",
    county="朝阳区",
    bank="中国工商银行北京朝阳支行",
    account="6222021234567890",
    account_mobile="13800138000"
)

# 发送请求
response = post_xml(
    "http://www-1.fuiou.com:28090/wmp/wxMchntMng.fuiou?action=wxMchntAdd",
    datagram
)
print(response)

# 创建支付订单
order_datagram = build_wx_pre_create_datagram(
    mchnt_cd="your_mchnt_cd",
    goods_des="测试商品",
    order_amt="1",  # 分
    term_ip="127.0.0.1",
    trade_type="JSAPI",
    openid="user_openid"
)

order_response = post_xml("https://fundwx.fuiou.com/wxPreCreate", order_datagram)
print(order_response)
```

## 环境变量配置

SDK 需要以下环境变量：

### 必需配置
- `FUIOU_INS_CD`: 机构号
- `FUIOU_MD5_KEY`: MD5签名密钥 (用于商户管理等接口)

### 可选配置
- `FUIOU_SUB_INS_CD`: 二级代理机构号
- `FUIOU_MCHNT_ID`: 商户号
- `FUIOU_NOTIFY_URL`: 支付回调URL
- `WX_APPID`: 微信公众号AppID
- `ALI_APPID`: 支付宝小程序AppID
- `PRIVATE_KEY`: RSA私钥 (用于支付订单签名)

### OSS配置 (用于附件上传)
- `OSS_ENDPOINT`: OSS端点
- `OSS_BUCKET`: OSS存储桶
- `OSS_REGION`: OSS区域

## API 文档

### 商户管理

#### 添加商户
```python
from fuiou_sdk import build_mchnt_add_datagram

datagram = build_mchnt_add_datagram(
    mchnt_name="商户姓名",
    mchnt_shortname="商户简称",
    id_card="身份证号",
    id_addr="身份证地址",
    start_dt="身份证开始日期(YYYYMMDD)",
    expire_dt="身份证到期日期(YYYYMMDD)",
    contact_mobile="联系手机号",
    addr="联系地址",
    city="城市",
    county="区县",
    bank="开户银行",
    account="银行账号",
    account_mobile="银行预留手机号"
)
```

#### 商户名称检查
```python
from fuiou_sdk import build_machnt_name_check_datagram

datagram = build_machnt_name_check_datagram("商户名称")
```

### 电子协议

#### 生成电子协议
```python
from fuiou_sdk import build_elec_contract_generate_datagram

datagram = build_elec_contract_generate_datagram("商户号")
```

#### 签署电子协议
```python
from fuiou_sdk import build_elec_contract_sign_datagram

datagram = build_elec_contract_sign_datagram(
    mchnt_cd="商户号",
    verify_no="验证码",
    contract_no="协议编号"
)
```

### 支付订单

#### 创建预订单
```python
from fuiou_sdk import build_wx_pre_create_datagram

datagram = build_wx_pre_create_datagram(
    mchnt_cd="商户号",
    goods_des="商品描述",
    order_amt="订单金额(分)",
    term_ip="终端IP",
    trade_type="JSAPI",  # 或 "FWC"
    openid="用户OpenID"
)
```

### 查询接口

#### 渠道子商户号查询
```python
from fuiou_sdk import build_chnl_sub_mch_id_query_datagram

datagram = build_chnl_sub_mch_id_query_datagram("商户号", "1")  # 1=微信, 2=支付宝
```

#### 认证查询
```python
from fuiou_sdk import build_wx_auth_query_datagram, build_ali_auth_query_datagram

wx_datagram = build_wx_auth_query_datagram("商户号")
ali_datagram = build_ali_auth_query_datagram("商户号")
```

### 工具函数

#### XML转JSON
```python
from fuiou_sdk import xml_to_json

result = xml_to_json(xml_string)
```

#### 附件上传
```python
from fuiou_sdk import upload_image

upload_image(
    mchnt_cd="商户号",
    id_card_front_image="身份证正面.jpg",
    id_card_back_image="身份证反面.jpg",
    inner_image="门脸照片.jpg",
    outer_image="门头照片.jpg",
    bank_card_front_image="银行卡正面.jpg"
)
```

## 开发环境

```bash
# 安装开发依赖
uv sync

# 运行测试
uv run pytest

# 代码格式化
uv run black src/
uv run isort src/

# 类型检查
uv run mypy src/
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题请联系: your.email@example.com
