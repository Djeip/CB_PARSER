import requests
import pandas as pd
import time


def LOMBARDS():
    DIR_PATH = time.strftime('%Y_%m_%d')
    URL = 'https://cbr.ru/vfs/finmarkets/files/supervision/list_PS.xlsx'

    FILE_NAME = "T_IN_PARSING_REESTR_LOMBARD.xlsx"

    nm = """C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/INPUT/""" + DIR_PATH + """/""" + FILE_NAME
    resp = requests.get(URL)

    with open(nm, 'wb') as f:
        f.write(resp.content)

    df = pd.read_excel(nm, header=2).drop(columns='№ п/п').rename(columns={
        'Дата внесения Банком России сведений о юридическом лице в реестр': 'DATAVNESEN',
        'Полное фирменное наименование': 'NAIMPOLN',
        'Сокращенное фирменное наименование': 'NAIMSOKR',
        'Адрес, указанный в едином государственном реестре юридических лиц': 'ADR',
        'Адрес электронной почты': 'EMAIL',
        'ОГРН': 'OGRN',
        'ИНН': 'INN',
        'Адреса официальных сайтов в информационно-телекоммуникационной сети «Интернет»': 'WEBSITE',
        'Номер контактного телефона': 'PHONE',

    })

    df['LOAD_DT'] = time.strftime('%Y-%m-%d')

    return df
