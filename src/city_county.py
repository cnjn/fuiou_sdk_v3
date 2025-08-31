
with open(__file__.replace("city_county.py", "富友省市区代码20250212.csv"), "r", encoding='utf-8') as f:
    f = f.readlines()[1:]
city_county = []
for i in f:
    test = [x.strip() for x in i.split(" ,")]
    city_county.append(test)

def get_city_code(city: str):
    for i in city_county:
        if i[1].endswith(city):
            return i[1].split(",")[0]
    return ""

def get_county_code(county: str):
    for i in city_county:
        if i[2].endswith(county):
            return i[2].split(",")[0]
    return ""

if __name__ == "__main__":
    print(get_city_code("玉溪市"))
    print(get_county_code("泸西县"))