# -*- coding: UTF-8 -*-
import requests
import json
import re


def parse(sentence):
    """Parse a sentence with a remote corenlp server"""
    text = sentence.encode("utf-8")

    properties = {
    'pipelineLanguage': 'zh',
    'annotators':'tokenize,ssplit,pos,parse,depparse, openie'
    }
    request_params = {"properties": json.dumps(properties)}
    res= requests.post('http://140.109.19.191:9000/', data=text, params=request_params)
    res = res.json()
    return res

def load_raw_data(filename):  # load the json data to list(dict()) for MATH 23K
    print("Reading lines...")
    f = open(filename, encoding="utf-8")
    js = ""
    data = []
    all_original_text = []
    for i, s in enumerate(f):
        js += s
        i += 1
        if i % 7 == 0:  # every 7 line is a json
            data_d = json.loads(js)
            if "千米/小时" in data_d["equation"]:
                data_d["equation"] = data_d["equation"][:-5]
            data.append(data_d)
            js = ""

    for sent in data:
        all_original_text.append(sent["original_text"])
        
    return all_original_text



def load_data(path):
    print('Reading lines...')
    all_original_text = []
    with open(path,'r') as f:
        problem_list = json.load(f)
    for problem in problem_list:
        all_original_text.append(problem['original_text'])
    return all_original_text

all_original_text = load_data("data/geometry_mwps.json")
# all_original_text = load_data("data/Math23K_geometry.json")


def get_tokens_and_dependencies(all_original_text):
    processed_data = []
    for sent in all_original_text:
        tmp = dict()
        res = parse(sent)
        tmp["tokens"] = res["sentences"][0]["tokens"]
        tmp["dependencies"] = res["sentences"][0]["basicDependencies"]
        processed_data.append(tmp)
    return processed_data

def get_num_position(tokens):
    group_num = []
    for token in tokens:
        idx, word, pos = token["index"], token["word"], token["pos"]
        if pos == "CD":
            pattern = re.compile("\d*\(\d+/\d+\)\d*|\d+\.\d+%?|\d+%?")
            is_digit = re.search(pattern, word)
            if is_digit:
                group_num.append(idx)
            elif word == "多少" or word == '几':
                group_num.append(idx)
    return group_num

processed_data = get_tokens_and_dependencies(all_original_text)

for sent in processed_data:
    sent["group_num"] = get_num_position(sent["tokens"])

def find_dependency(data, id = 0):
    dependency_list = ['dobj', 'aux:asp', 'advmod', 'nsub', 'dep', 'mark:clf']
    pos_list = ['VV', 'VC', 'DT']
    tmp = []
    if id != 0:
        if data['tokens'][id-1]['pos'] in pos_list:
            for dep in data['dependencies']:
                start_id, end_id, dep, group_num = dep["governor"], dep["dependent"], dep["dep"], data['group_num']
                if (start_id == id) and (dep in dependency_list):
                    tmp.extend(find_dependency(data, end_id))
        tmp.append(id)
        return tmp

    for dep in data['dependencies']:
        start_id, end_id, dep, group_num = dep["governor"], dep["dependent"], dep["dep"], data['group_num']
        if start_id == 0:
            continue
        if start_id in group_num:
            if dep == 'mark:clf':
                tmp.append(end_id)
                continue
        if end_id in group_num:
            if dep == 'dep':
                tmp.extend(find_dependency(data, start_id))
            elif data['tokens'][start_id-1]['pos'] == 'VV':
                tmp.extend(find_dependency(data, start_id))
            elif dep == 'nummod':
                tmp.extend(find_dependency(data, start_id))
    return tmp

problem_list = []
count = 0
for idx, sent in enumerate(processed_data):
    count += 1
    tmp = dict()
    sent['group_num'].extend(find_dependency(sent))
    sent['group_num'] = list(set(sent['group_num']))
    sent['group_num'].sort()
    tmp["id"] = str(count)
    tmp["group_num"] = sent["group_num"]
    problem_list.append(tmp)
    #print(idx, sent['group_num'])
#print(problem_list[0])

for problem in problem_list:
    tmp = []
    for num in problem['group_num']:
        tmp.append(num-1)
    problem['group_num'] = tmp

#print(problem_list[0])

with open("geometry_mwps_processed.json", 'w', encoding='utf-8') as f:
    json.dump(problem_list, f, ensure_ascii = False, indent = 4)