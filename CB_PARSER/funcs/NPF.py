import pandas as pd
import time



def NPF(DIR_PATH):
    DIR_PATH= time.strftime('%Y_%m_%d')
    URL = 'https://www.asv.org.ru/download/?type=document&id=154630'
    dt_url = 'https://cbr.ru/registries/RSCI/activity_npf/#a_85257link'

    FILE_NAME = "T_IN_PARSING_REESTR_NPF.xlsx"

    FILE_NAME_OUT = "T_IN_PARSING_REESTR_NPF.csv"

    DATE = time.strftime('%d.%m.%Y')

    wget.download(URL, """./INPUT/""" + DIR_PATH + """/""" + FILE_NAME)
    df = pd.read_excel("""./INPUT/""" + DIR_PATH + """/""" + FILE_NAME, header=3).drop(
        columns=['Unnamed: 10', 'Unnamed: 11']).rename(columns={
        1: 'REESTR_NUM',
        2: 'DATAVNES',
        3: 'NAIMPOLN',
        4: 'LIC_NUM',
        5: 'INN',
        6: 'OGRN',
        7: 'ADDRESS',
        8: 'WEBSITE',
        9: 'DATAISKL',
        10: 'NOTES'
    })

    df['LOAD_DT'] = time.strftime('%Y-%m-%d')

    return df
