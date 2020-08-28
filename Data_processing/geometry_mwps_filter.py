import json

def read_json(path):
    with open(path,'r') as f:
        file = json.load(f)
    return file

def load_raw_data(filename):  # load the json data to list(dict()) for MATH 23K
    print("Reading lines...")
    f = open(filename, encoding="utf-8")
    js = ""
    data = []
    for i, s in enumerate(f):
        js += s
        i += 1
        if i % 7 == 0:  # every 7 line is a json
            data_d = json.loads(js)
            if "千米/小时" in data_d["equation"]:
                data_d["equation"] = data_d["equation"][:-5]
            data.append(data_d)
            js = ""

    return data

data_23k = load_raw_data("data/Math_23K.json")

keyword = ['正方', '长方', '圆', '平行四边', '面积', '体积', '边长', '周长', '宽', '立方', '形']
count = 0
problem_list = []
for problem in data_23k:
    if '3.14' in problem['equation']:
        count += 1
        tmp = problem
        tmp['id'] = count
        problem_list.append(problem)
        continue
    for word in keyword:
        if word in problem['original_text']:
            count += 1
            tmp = problem
            tmp['id'] = count
            problem_list.append(problem)
            break

with open("Math23K_geometry.json", "w", encoding='utf-8') as f:
    json.dump(problem_list, f, ensure_ascii = False, indent = 4 )