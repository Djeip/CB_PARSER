import requests
import pandas as pd
import time


def CBR_CREDIT_ORG():
    res = requests.get('https://www.cbr.ru/banking_sector/credit/FullCoList/')

    tbl = pd.read_html(res.text)
    df = pd.DataFrame(tbl[0]).drop(columns='№ п/п').rename(columns={
        "Вид": "VID",
        "Регистрационный номер": "REG_NUM",
        "ОГРН": "OGRN",
        "Наименование": "NAIM",
        "Организационно-правовая форма": "OPF",
        "Дата регистрации Банком России": "DATA_REG",
        "Статус лицензии": "LIC_STAT",
        "Местонахождение": "ADDRESS"
    })
    df['LOAD_DT'] = time.strftime('%Y-%m-%d')

    return df
