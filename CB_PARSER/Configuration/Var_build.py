# ================================ Настройки подключения к БД, куда пишем результаты парсинга ========================
postgre = {
    "pass": 1987,
    "host": 'localhost',
    "port": 5432,
    "db": 'postgres'
}

# ============================ Основной адрес для папки с результатами и названия папок по проектам ==================
main_folder = 'c:\\Users\\Администратор\\Documents\\Parsing_Data\\'
folder_name_data = 'Data'
folder_name_data_cbr = 'CBR'
folder_data_cbr_calendar = 'CBR_calendar'
folder_data_cbr_ko = 'CBR_ko'
folder_data_cbr_structure = 'CBR_structure'
folder_data_nash_dom_rf = 'Nash_Dom_RF'
folder_data_cbr_reestr = 'CBR_Reestr'

# =================================== Адреса для отправки результатов =================================================
#email_send = 'shuvalov.dm.al@sber.ru'
email_send = 'ishirokov@sberbank.ru'
# ======================================== User-agent для парсинга ====================================================
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'

    ]

list_proxy = [
                {'IP':'95.181.157.98:8000', 'login':'3MCqMT', 'pas':'taYnxY'},
                {'IP':'95.181.157.111:8000', 'login':'3MCqMT', 'pas':'taYnxY'},
                {'IP':'95.181.155.25:8000', 'login':'3MCqMT', 'pas':'taYnxY'},
                {'IP':'194.67.210.203:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'194.67.210.13:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'194.67.211.204:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'194.67.210.87:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'194.67.210.167:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'194.67.211.194:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'194.67.212.62:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'194.67.209.185:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'95.181.157.111:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'194.67.210.200:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'194.67.210.247:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'95.181.157.111:8000', 'login':'GyXar9', 'pas':'MbPmCa'},
                {'IP':'194.67.210.100:8000', 'login':'GyXar9', 'pas':'MbPmCa'}]