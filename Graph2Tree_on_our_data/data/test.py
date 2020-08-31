import json

def read_json(path):
    with open(path,'r') as f:
        file = json.load(f)
    return file

group_num = read_json('geometry_mwps_processed.json')
for i in group_num:
    tmp = []
    for num in i['group_num']:
        num += 1
        tmp.append(num)
    i['group_num'] = tmp

with open("geometry_mwps_processed_r.json", 'w', encoding='utf-8') as f:
    json.dump(group_num, f, ensure_ascii = False, indent = 4)