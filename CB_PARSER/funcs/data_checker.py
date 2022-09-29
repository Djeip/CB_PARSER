from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import re
import json


def date_parser(act, URL, XPATH, pat):
    res = requests.get(URL)
    soup = bs(res.text, 'lxml')
    tree = etree.HTML(str(soup))
    dt = str(tree.xpath(XPATH)[0])

    if pat != '':
        dt = re.findall(pat, dt)[0]

    return datetime.strptime(act, '%d.%m.%Y') >= datetime.strptime(dt, '%d.%m.%Y')


def date_checker():
    with open(r'C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/PAGES.json', 'r', encoding='utf-8') as f1:
        pages = json.load(f1)
    with open(r'C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/ACT_DATE.json', 'r',
              encoding='utf-8') as f2:
        act_date = json.load(f2)

    for key in pages.keys():
        tmp = pages.get(key)
        act = act_date.get(key)
        pages[key]['ACTUAL'] = date_parser(act, tmp['URL'], tmp['XPATH'], tmp['PAT'])

    with open(r'C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/PAGES.json', 'w', encoding='utf-8') as f3:
        json.dump(pages, f3)

    # TODO: Более красивый JSON
    return pages
