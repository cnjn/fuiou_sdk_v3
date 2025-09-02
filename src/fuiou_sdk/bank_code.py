

with open(__file__.replace("bank_code.py", "附件9 联行号(20241218更新).csv"), "r", encoding="utf-8") as f:
    lines = f.readlines()

bank_data = []
for line in lines:
    parts = [x.strip() for x in line.strip().split(",")]
    if len(parts) >= 4:
        bank_data.append(parts)

def get_bank_code(bank_name: str):
    """
    根据银行名称获取银行代码
    :param bank_name: 银行名称
    :return: 银行代码，如果未找到返回空字符串
    """
    for row in bank_data:
        if len(row) >= 4 and bank_name == row[3]:
            return row[2]
    return ""

if __name__ == "__main__":
    print(get_bank_code("中国工商银行云南红河分行泸西城区支行"))
    print(get_bank_code("中国建设银行股份有限公司福州宁化支行"))
