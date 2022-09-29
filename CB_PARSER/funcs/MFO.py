import requests
import wget
import pandas as pd
import time


def MFO():
    DIR_PATH= time.strftime('%Y_%m_%d')
    URL = 'https://cbr.ru/vfs/finmarkets/files/supervision/list_MFO.xlsx'

    FILE_NAME = "T_IN_PARSING_REESTR_MFO.xlsx"

    nm = """C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/INPUT/""" + DIR_PATH + """/""" + FILE_NAME
    resp = requests.get(URL)

    with open(nm, 'wb') as f:
        f.write(resp.content)

    df = pd.read_excel(nm, header=4, converters={
        'Регистрационный номер записи': str,
        'Основной государственный регистрационный номер': str,
        'Идентификационный номер налогоплательщика': str,
        'Unnamed: 2': str,
        'Unnamed: 3': str,
        'Unnamed: 4': str,
        'Unnamed: 5': str
    }).drop(columns='№ п/п')

    tmp = df[['Регистрационный номер записи', 'Unnamed: 2',
              'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5']]
    df['Регистрационный номер записи'] = tmp.fillna(
        '').apply(lambda x: ''.join(x), axis=1)

    df.drop(columns=['Unnamed: 2', 'Unnamed: 3',
                     'Unnamed: 4', 'Unnamed: 5'], inplace=True)

    df.rename(columns={
        'Регистрационный номер записи': 'REG_NUM',
        'Дата внесения сведений о юридическом лице в государственный реестр микрофинансовых организаций': 'DATAVNES',
        'Вид микрофинансовой организации': 'VID_MFO',
        'Основной государственный регистрационный номер': 'OGRN',
        'Идентификационный номер налогоплательщика': 'INN',
        'Полное наименование': 'NAIMPOLN',
        'Сокращенное наименование': 'NAIMSOKR',
        'Адрес, указанный в едином государственном реестре юридических лиц': 'ADDRESS',
        'Адреса официальных сайтов в информационно-телекоммуникационной сети "Интернет"': 'WEBSITE',
        'Номер контактного телефона': 'PHONE',
        'Адрес электронной почты': 'EMAIL',
    }, inplace=True)

    df['LOAD_DT'] = time.strftime('%Y-%m-%d')

    return df
