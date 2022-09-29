import os
import time
import json
import py7zr

from Configuration import MyTools_build as MT
from Configuration import Var_build as V

from funcs.CBR_CREDIT_ORG import CBR_CREDIT_ORG
from funcs.CBR_CREDIT_ORG_STRUC import CBR_CREDIT_ORG_STRUC
from funcs.KPK import KPK
from funcs.LOMBARDS import LOMBARDS
from funcs.MFO import MFO
from funcs.REESTR_FINORG_123 import REESTR_FINORG_123
from funcs.SPR_BIC import SPR_BIC
from funcs.SPR_BANK_DEP import SPR_BANK_DEP

# TODO: Уточнить насчет нпФ from funcs.NPF import NPF
from funcs.data_checker import date_checker


def daily():
    # DIR creation
    DATE_STR_FOR_DIR = time.strftime('%Y_%m_%d')

    MAIN_DIR = r'C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/'
    if not os.path.isdir(MAIN_DIR + """INPUT/""" + DATE_STR_FOR_DIR):
        os.mkdir(MAIN_DIR + """INPUT/""" + DATE_STR_FOR_DIR)
    if not os.path.isdir(MAIN_DIR + """OUTPUT/""" + DATE_STR_FOR_DIR):
        os.mkdir(MAIN_DIR + """OUTPUT/""" + DATE_STR_FOR_DIR)

    OUTPUT = MAIN_DIR + """OUTPUT/""" + DATE_STR_FOR_DIR

    status = []

    positive = (lambda x: f'Доступны обновления для таблицы {x.lower()}')
    negative = (lambda x: f'Таблица {x.lower()} актуальна')

    # Date actualisation
    act_dates = date_checker()

    def Save_and_send(flrezult_name, logs):
        f_path = f'DAILY_PARSING_{DATE_STR_FOR_DIR}.7z'
        fl_name_7z_path = os.path.join(MAIN_DIR + """OUTPUT""", f_path)
        with py7zr.SevenZipFile(fl_name_7z_path, 'w') as archive:
            archive.writeall(flrezult_name)
        MT.send_email(addr_to=V.email_send, msg_subj=f_path,
                      msg_text='; '.join(logs),
                      files=[fl_name_7z_path])

    # activation decorator
    def func_activation(func):
        def run(key=func.__name__):
            cur = act_dates.get(key)
            if not cur['ACTUAL']:
                act_dates.get(key)['ACTUAL'] = True

                status.append(positive(cur['NAIMRUS']))
                print(positive(cur['NAIMRUS']))

                df = func()
                df.to_csv(OUTPUT + '/' + cur['FILE_OUT'], sep=';',
                          header=True, index_label=False, index=False, encoding='utf-8')
                with open(r'C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/ACT_DATE.json', 'r',
                          encoding='utf-8') as f:
                    cur_date = json.load(f)
                cur_date[key] = time.strftime('%d.%m.%Y')

                with open(r'C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/ACT_DATE.json', 'w',
                          encoding='utf-8') as f:
                    json.dump(cur_date, f)
            else:
                status.append(negative(cur['NAIMRUS']))
                print(negative(cur['NAIMRUS']))

        return run

    # Parsing activation
    func_activation(CBR_CREDIT_ORG)()
    func_activation(CBR_CREDIT_ORG_STRUC)()
    func_activation(KPK)()
    func_activation(LOMBARDS)()
    func_activation(MFO)()
    func_activation(REESTR_FINORG_123)()
    func_activation(SPR_BIC)()
    func_activation(SPR_BANK_DEP)()

    # Pages info actualisation
    with open(r'C:\Users\Администратор\Documents\GitHub\POTENCIAL_DE_PARSING\PAGES.json', 'w') as outfile:
        json.dump(act_dates, outfile)

    # ZIP and send
    Save_and_send(OUTPUT, status)


# for i in status:
#     send_text = 'https://api.telegram.org/bot' + config.TOKEN + \
#         '/sendMessage?chat_id=' + config.CHAT_ID + '&parse_mode=Markdown&text=' + i
#     response = requests.get(send_text)


#  df.to_csv("""./OUTPUT/"""+DIR_PATH+"""/T_IN_PARSING_CBR_CREDIT_ORG.csv""", sep=';',
#            header=True, index_label=False, index=False, encoding='utf-8')

if __name__ == '__main__':
    daily()
