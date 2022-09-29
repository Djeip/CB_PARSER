from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from tqdm import tqdm


def url_getter():
    dt_url = 'https://www.cbr.ru/banking_sector/credit/FullCoList/'
    res = requests.get(dt_url)

    soup = bs(res.text, 'lxml')
    tmp = soup.find_all('tr')
    return list(map(lambda x: x.contents[9].contents[0].attrs['href'], tmp[1:]))


def tbl_parse(con_lst):
    def row_parse(row):
        row = row.contents
        try:
            r_nm = str(row[1].contents[0])
        except KeyError:
            r_nm = None

        try:
            r_val = str(row[3].contents[0])
        except KeyError:
            r_val = None

        return {
            'row_id': r_nm,
            'val': r_val
        }

    res = list(map(row_parse, con_lst[:6]))
    res[-2]['val'] = res[-2]['val'].split(' ')[0]
    return pd.DataFrame(res)['val'].values


def SPR_BANK_DEP():
    urls = url_getter()
    data_output = []
    for i in tqdm(urls):
        dt_url = 'https://www.cbr.ru/' + i
        res = requests.get(dt_url)

        soup = bs(res.text, 'lxml')
        tmp = soup.find_all('div', {'class': 'coinfo_item row'})
        data_output.append(tbl_parse(tmp))

    df = pd.DataFrame(data_output).rename(columns={
        0: 'NAIMPOLN', 1: 'NAIMSOKR', 2: 'REG_NUM', 3: 'DATAREG', 4: 'OGRN', 5: 'BIC', })

    return df
