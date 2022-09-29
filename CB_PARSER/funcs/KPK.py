import requests
import pandas as pd
import time


def KPK():
    DIR_PATH= time.strftime('%Y_%m_%d')
    URL = 'https://cbr.ru/vfs/finmarkets/files/supervision/list_KPK_gov.xlsx'

    FILE_NAME = "T_IN_PARSING_REESTR_KPK.xlsx"

    nm = """C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/INPUT/""" + DIR_PATH + """/""" + FILE_NAME
    resp = requests.get(URL)

    with open(nm, 'wb') as f:
        f.write(resp.content)

    df = pd.read_excel(nm, header=1, converters={
        'ОГРН': str,
        'ИНН': str,
        'КПП': str,
        'ОГРН  саморегулируемой организации в сфере финансового рынка': str
    }).drop(columns='№ п/п').rename(columns={
        'Дата внесения сведений в единый государственный реестр юридических лиц': 'DATAVNES',
        'Способ образования юридического лица': 'SPOSOBOBR',
        'Полное наименование': 'NAIMPOLN',
        'Сокращенное наименование': 'NAIMSOKR',
        'Наименование субъекта Российской Федерации': 'REGION_NAME',
        'Адрес, указанный в едином государственном реестре юридических лиц': 'ADDRESS',
        'ОГРН': 'OGRN',
        'ИНН': 'INN',
        'КПП': 'KPP',
        'Статус юридического лица': 'ULSTATUS',
        'Сведения о лице, имеющем право без доверенности действовать от имени кооператива': 'SVEDFL',
        'Наименование саморегулируемой организации в сфере финансового рынка, членом которой является (являлся) кооператив': 'NAIMSAMOREG',
        'ОГРН  саморегулируемой организации в сфере финансового рынка': 'OGRNSAMOREG',
        'Дата приема в члены саморегулируемой организации в сфере финансового рынка': 'DATAPRIEM',
        'Дата исключения': 'DATAISKL',
        'Основание прекращения членства в саморегулируемой организации в сфере финансового рынка': 'OSNPREK',
        'Сведения о том, что число членов (общее число членов и ассоциированных членов) кооператива превысило три тысячи физических и (или) юридических лиц': 'SVED',
    })

    df['LOAD_DT'] = time.strftime('%Y-%m-%d')
    return df
