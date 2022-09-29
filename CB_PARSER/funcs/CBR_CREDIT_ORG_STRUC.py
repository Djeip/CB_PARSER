import requests
import pandas as pd
import time


def CBR_CREDIT_ORG_STRUC():
    res = requests.get('https://www.cbr.ru/banking_sector/credit/cstat/')
    tbl = pd.read_html(res.text)
    df = pd.DataFrame(tbl[0]).rename(columns={"Вид": "VID",
                                              "Регион": "REGION",
                                              "Наименование КО": "NAIMKO",
                                              "Рег. № КО": "REG_NUM_KO",
                                              "Головные офисы": "GOLOVA",
                                              "Филиалы": "FILIALS",
                                              "Допофисы": "DOPOFIS",
                                              "Всего подразделений": "SUM_PODR"
                                              })
    df['LOAD_DT'] = time.strftime('%Y-%m-%d')
    df = df[df.REGION != df.NAIMKO].reset_index(drop=True)
    return df
