import requests
import pandas as pd
import time


def REESTR_FINORG_123():
    DIR_PATH = time.strftime('%Y_%m_%d')
    URL = 'https://cbr.ru/vfs/finmarkets/files/supervision/list_123_fz.xlsx'
    FILE_NAME = "T_IN_PARSING_REESTR_FINORG_123.xlsx"

    nm = """C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/INPUT/""" + DIR_PATH + """/""" + FILE_NAME
    resp = requests.get(URL)

    with open(nm, 'wb') as f:
        f.write(resp.content)

    df = pd.read_excel(nm, sheet_name="КПК",
                       header=3,
                       converters={'Unnamed: 6': str, 'Unnamed: 7': str}).drop(columns='Unnamed: 0').rename(columns={
        "Unnamed: 1": "NAIMPOLN",
        "Unnamed: 2": "NAIMSOKR",
        "Unnamed: 3": "ADDRESS",
        "Unnamed: 4": "SITE",
        "Unnamed: 5": "TEL",
        "Unnamed: 6": "INN",
        "Unnamed: 7": "OGRN",
        "Регистрационный номер записи": "REGNOMZAP",
        "Дата внесения сведений в реестр ": "DATASVEDREEST",
        "Вид деятельности": "VIDDEYAT",
        "Unnamed: 11": "FINUSLUG",
        "Unnamed: 12": "OTMETKA",
        "Unnamed: 13": "DATAOBR",
    })

    df['LOAD_DT'] = time.strftime('%Y-%m-%d')

    return df
