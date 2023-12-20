import os
import requests
import json
from tqdm import tqdm
from collections import OrderedDict

with open('/mnt/p3_translate/proxies.txt','r') as f:
    lst_proxies = f.readlines()
lst_proxies = ['http://'+ x.replace('\n','') for x in lst_proxies ]

data = json.load(open('/mnt/p3_translate/DS_merged_data_deduplicated.json', 'r'))


def translate_gg_free(text, tgt_lang = "en", src_lang = "vi"):
    txt = str(text)
    proxies = {
        "http": lst_proxies
    }
    tran = ''
#     for txt in texts:
    try:
        r = requests.get(
            'https://translate.googleapis.com/translate_a/single?client=gtx&sl=' + src_lang + '&tl=' + tgt_lang +
            '&dt=t&dt=bd&dj=1&q=' + txt, proxies=proxies)
        if r.status_code == 200:
            resp = r.json()
            for j in resp['sentences']:
                tran += j['trans'] + " "
    except Exception as ve:
        print(ve)
    return tran


def translate(example):
    return translate_gg_free(example)


def get_requirement(example):
    unique_ordered_dict = OrderedDict.fromkeys(example)

    unique_list = list(unique_ordered_dict.keys())    
    
    text = ''
    for item in unique_list:
        text += ' ' + item

    return text    
        
list_re = []
count = 0
for item in tqdm(data):
    if get_requirement(item['requirements']) != '':
        trans = translate(get_requirement(item['requirements']))
        if len(trans.split(' ')) > 20:
            list_re.append({
                'label': item['keyword'],
                'requirements': trans,
            })
            print(count)
            count += 1
            
json.dump(list_re, open('/mnt/p3_translate//text.json', 'w'), ensure_ascii=False)       
count
    