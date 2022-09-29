# вер 2.5.0

import logging


def reload_module(nm_module):
    """
    Перезагружаем модулью
    """

    from importlib import reload

    otv = reload(nm_module)

    return otv


def send_email(addr_to, msg_subj, msg_text, files=None, addr_from='dmitry.shuvalow@mail.ru',
               password='DmfZZ97V85aHEsThQe6L'):
    """
    Отправка писем с вложениями
    :addr_to: От кого
    :msg_subj: Заголовок
    :msg_text: Текст сообщения
    :files: Вложенные сообщения
    """
    import smtplib  # Импортируем библиотеку по работе с SMTP
    import os  # Функции для работы с операционной системой, не зависящие от используемой операционной системы

    # Добавляем необходимые подклассы - MIME-типы
    import mimetypes  # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
    from email import encoders  # Импортируем энкодер
    from email.mime.base import MIMEBase  # Общий тип
    from email.mime.text import MIMEText  # Текст/HTML
    from email.mime.image import MIMEImage  # Изображения
    from email.mime.audio import MIMEAudio  # Аудио
    from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект

    def attach_file(msg, filepath):  # Функция по добавлению конкретного файла к сообщению
        filename = os.path.basename(filepath)  # Получаем только имя файла
        ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
        if ctype is None or encoding is not None:  # Если тип файла не определяется
            ctype = 'application/octet-stream'  # Будем использовать общий тип
        maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
        if maintype == 'text':  # Если текстовый файл
            with open(filepath, encoding='utf-8') as fp:  # Открываем файл для чтения
                file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
                fp.close()  # После использования файл обязательно нужно закрыть
        elif maintype == 'image':  # Если изображение
            with open(filepath, 'rb') as fp:
                file = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'audio':  # Если аудио
            with open(filepath, 'rb') as fp:
                file = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
        else:  # Неизвестный тип файла
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
                encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
        file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
        msg.attach(file)

    def process_attachement(msg, files):  # Функция по обработке списка, добавляемых к сообщению файлов
        for f in files:
            if os.path.isfile(f):  # Если файл существует
                attach_file(msg, f)  # Добавляем файл к сообщению
            elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
                dir = os.listdir(f)  # Получаем список файлов в папке
                for file in dir:  # Перебираем все файлы и...
                    attach_file(msg, f + "/" + file)

    # ======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
    server = smtplib.SMTP('smtp.mail.ru', 25)  # Создаем объект SMTP
    server.starttls()  # Начинаем шифрованный обмен по TLS
    # server.set_debuglevel(True)                            # Включаем режим отладки, если не нужен - можно закомментировать
    server.login(addr_from, password)  # Получаем доступ

    # ==========================================================================================================================

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = msg_subj  # Тема сообщения

    body = msg_text  # Текст сообщения
    msg.attach(MIMEText(body, 'plain', 'utf-8'))  # Добавляем в сообщение текст
    if files:
        process_attachement(msg, files)

    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим


def get_requests(url, log_debug, log_rezult, mode_proxy=0, to_json=False, list_proxy=None, user_agent_list=None
                 , time_slip=5):
    """
    Полученние данных с нужной страницы интернета
    :param url: Адрес страницы, данные с которой необходимо получить
    :mode_proxy: Режим работы прокси. 0 - прокси не используется, 1 - используется прокси. По умолчанию 0
    :param to_json: Если True то результат запроса преобразуется в json. По умолчанию False
    :return: Результат запроса
    """
    TODO: "Надо прописать ветку, когда mode_proxy = 0 и user-agent не прописан"

    import random
    import requests
    import time

    # фиктивные user-agent

    otv = None
    user_agent = random.choice(user_agent_list)
    log_debug.info(f"Выбран user_agent = {user_agent}")

    if mode_proxy == 0:
        otv = requests.get(url=url, headers={'us0er-agent': user_agent})
    elif mode_proxy == 1:

        flag = False
        total_proxi = len(list_proxy)
        kol = 0
        while not flag and kol <= total_proxi:
            try:
                prox_infa = random.choice(list_proxy)
                log_debug.info(f"Выбран прокси = {prox_infa['IP']}")
                prox = {
                    'https': f"http://{prox_infa['login']}:{prox_infa['pas']}@{prox_infa['IP']}"
                }
                time.sleep(random.randint(1, time_slip))
                log_debug.info(f"Выбран user_agent = {user_agent}")
                otv = requests.get(url=url, headers={'user-agent': user_agent}, proxies=prox)
                #
                flag = True
            except:
                flag = False
                log_debug.debug(f"Ошибка подключения proxy {prox_infa['IP']}")

    if to_json:
        if otv:
            otv = otv.json()

    return otv


def folder_exists(folder_name, log_debug=None, log_rezult=None):
    """
    Процедура проверяет наличие указанной папки (полный адрес + название папки)
    Если папка есть - выводиться соответствующее уведомление.
    Если папки нет - она создается.
    :param folder_name: Полный путь + название папки
    :return: Ничего. Происходят операции с папками
    """
    import os

    if os.path.exists(folder_name):
        if log_debug:
            log_debug.info(f"Папка {folder_name} уже существует!")
    else:
        os.makedirs(folder_name)
        if log_rezult:
            log_rezult.info(f'Создана папка {folder_name}')


def get_json_from_file(fl_path, log_debug, log_rezult, code='utf-8'):
    """
    Читается файл и полученные данные преобразуются в json формат.
    Работает в связке с функцией save_to_json_file
    :param fl_path: Полный путь до файла, который наодо преобразовать в json
    :param code: Кодировка чтения файла, по умолчанию utf-8
    :return: Данные в формате json
    """
    import json

    otv = None
    with open(fl_path, 'r', encoding=code) as file:
        otv = json.load(file)
    log_debug.info(f'Сформировали из файла {fl_path} массив json')
    return otv


def save_to_json_file(fl_path, data, log_debug, log_rezult, param='w', code='utf-8'):
    """
    Сохранение массива данных в файл json. Работает в связке с функцией get_json_from_file
    :param fl_path: Полный путь до файла, который наодо преобразовать в json
    :param data: Массив данных для сохранения в файл json
    :param param: Способ записи: 'a' - добавление; 'w' - перезапись существующего файла или создание нового. По умолчанию 'w'
    :param code: Кодировка чтения файла, по умолчанию utf-8
    :return: Ничего. Файл сохраняется на диск
    """

    import json
    fl_path = '.'.join([fl_path, 'json'])
    with open(fl_path, param, encoding=code) as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    log_debug.info(f'Сохранили в файл json {fl_path} в данные')


def setup_logger(name, log_file, level=logging.NOTSET, file_mode='w'):
    """
        Функция по настройке нескольких loggerov с разными файлами логирования
        :param name: Имя логгера
        :param log_file: Файл для сохранения логов
        :param level: Уровень логирования
        :return: Настроенный логгер
        """

    import logging

    logging.basicConfig(datefmt='%d.%m.%Y %H:%M:%S')

    log_format = logging.Formatter('%(asctime)s | %(levelname)s | %(funcName)s | %(lineno)s | %(message)s')

    handler = logging.FileHandler(log_file, encoding='utf-8', mode=file_mode)
    handler.setFormatter(log_format)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def dt_end_of_file(nm='File', en='.txt'):
    from datetime import datetime
    otv = None
    now = datetime.now()
    date_time = now.strftime("%Y%m%d %H%M%S")
    otv = '_'.join([nm, date_time])
    otv = ''.join([otv, en])
    return otv


def now_str(rezim=0):
    from datetime import datetime
    otv = None
    now = datetime.now()
    if rezim == 0:
        date_time = now.strftime("%Y%m%d %H%M%S")
    elif rezim == 1:
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    elif rezim == 2:
        date_time = now.strftime("%Y-%m-%d")
    elif rezim == 3:
        date_time = now.strftime("%Y%m%d")

    return date_time


def Obhod_folder(path, regim=0, find=[], iskl=[]):
    """\
    Функция проходит по всем папкам/подпапкам по переданному пути. Возвращает список файлов во всех директориях (в формате, путь к файлу, название файла)

    :path анализируемый путь
    :regim режим, в котором обрабатывается папка. 0 - анализируются все подпапки, без ограничений по уровню вложенности (по умолчанию), 1 - список файлов входящей папки;
    :find список расширений, среди по которым будут возвращены результаты
    :iskl список исключений, которые опускаются из результирующего множетсва
    :return Список файлов вс всех папках / подпапках передаваемого пути
    """

    import os

    itog = []

    for folderName, subfolders, filenames in os.walk(path):
        if regim == 0 and subfolders:
            for subfolder in subfolders:
                itog = itog + Obhod_folder(os.path.join(path, subfolder))
        else:
            for filename in filenames:
                rash = '.' + filename.split('.')[-1]
                if find and iskl:
                    if rash in find and rash not in iskl:
                        itog.append([folderName, filename])
                    elif find and not iskl:
                        if rash in find:
                            itog.append([folderName, filename])
                    elif iskl and not find:
                        if rash in iskl:
                            itog.append([folderName, filename])
                elif not iskl and not iskl:
                    itog.append([folderName, filename])
        return itog


def Del_old_log(path, regim=1, gran=3):
    from datetime import datetime
    import os

    """\
        Функция очистки файлов исходя из времени их создания. Наприме, удаление старых лог-журналов.

        :path Путь к папке в которой нужно осуществить очистку
        :regim Способ определения возраста файла: 
            0 - дата зашита в название файла (по умолчанию), 
            1 - дата создания файла, 
            2 - дата изменения файла, 
            3 - комбинированный способ (название - создания - изменения)
        :return Ничего не возвращает, только удаляет файлы
        """

    """\
    За основу берется информация получаемая из os.stat(file) - это:
        st_atime/st_atime_ns - время последнегно доступа, выраженное в секундах (в наносекундах как целое число)
        st_ctime / st_ctime_ns - время создания в Windows, выраженное в секундах (в наносекундах как целое число)
        st_dev - Индентификатор устройства, на котором находится этот файл
        st_gid - Индентификатор группы владельца файла
        st_mode  - режим файла (быт типа файла и бит режима файла)
        st_mtime / st_mtime_ns - Время последнего изменения содержимого, выраженное в секунда (в наносекундах как целое число)
        st_nlink - Количество жестких ссылок
        st_size - Размер файла в байтах, если он является обычным файлом или символической ссылкой. Рамер символической ссылки - это длина имени пути, которое она содержит, без конечного нулевого байта
        st_uid - Идентификатор пользователя владельца файла
    """

    tek_data = datetime.today()

    list_file = Obhod_folder(path, regim=1)
    if list_file:
        for fl in list_file:
            file = os.path.join(fl[0], fl[1])
            stat = os.stat(file)
            if regim == 0:
                pass
            elif regim == 1:
                st_time = datetime.fromtimestamp(stat.st_ctime)
            elif regim == 2:
                st_time = datetime.fromtimestamp(stat.st_mtime)
            elif regim == 3:
                pass
            if (tek_data - st_time).days > gran:
                os.remove(file)


formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(funcName)s;%(lineno)s;%(message)s')


def PrintException():
    """
	Функция для информативного сообщения об ошибки (в каком файле, строке возникла ошибка и какое сообщение 
	выводит программа.
	"""
    import sys
    import linecache

    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return ('Ошибка в файле {}, строка {} "{}": {}'.format(filename, lineno, line.strip(), exc_obj))


def Try_to(func, log_debug, log_rezult, rezim_try=0, rezim_convert='txt', rezim_otveta='None', date_format=None):
    """
    Обертка try для выполнения функций

    :rezim_try: Режим проверки. По умолчанию 0
    0 - обычное try ... except

    :rezim_convert: Режим конвертации финального значения. По умолчанию txt
    'txt' - текстовое значение
    'int' - целое число
    'float' - дробное число
    'date' - дата

    :rezim_otveta: Какое значение возращается, если функция не отработала или пустое значение. По умолчанию 'None'
    'None' - вернется --> None
    'txt' - вернется --> ''
    'int' - вернется --> 0
    'float' - вернется --> 0
    'date' - вернется --> текущая

    :date_format: строка по формату разбора, например '%d-%m-%Y'
    %y - год из двух цифр (от 00 до 99)
    %Y - год из четырех цифр (например, '2021')
    %m - номер месяца с предваряющим нулем (от 01 до 12)
    %b - аббревиатура месяца в заивимости от настроек локали (например, "янв" для января)
    %B - название месяца в зависимости от настроек локали (например, "Январь")
    %d - номер дня в месяце с предваряющим нулем (от "01" до "31")
    %j - день с начала года (от "001" до "366")
    %U - номер недели в году (от "00" до "53"). Неделя начинается с воскресенья. Все дни с начала года до первого воскресенья относятся к неделе с номером "0"
    %W - номер недели в году (от "00" до "53"). Неделя начинается с понедельника. Все дни с начала года до первого понедельника относятся к неделе с номером "0"
    %w - номер дня недели ("0" - воскресенье, "6" - суббота)
    %a - аббревиатура дня недели в зависимости от настроек локали ("Пн" для Понедельника)
    %A - название дня недели в зависимости отн сатроек локали ("Понедельник")
    %H - часы в 24-часовом формате (от "00" до "23")
    %I - часи в 12-часовом формате (от "01" до "12")
    %M - минуты (от "00" до "59")
    %S - секунды (от "00" до "59")
    %p - эквивалент значениям AM и PM в текущей локали
    """
    from datetime import datetime

    def Rezim_otveta(rezim_otveta):
        match rezim_otveta:
            case 'None':
                otv = None
            case 'txt':
                otv = ''
            case 'int':
                otv = 0
            case 'float':
                otv = 0
            case 'date':
                otv = datetime.now()
        return otv

    if rezim_try == 0:
        try:
            otv = func
        except:
            otv = None
            log_debug.debug(f'Ошибка выполнения операции {str(func)}\t {PrintException()}')

    match rezim_convert:
        case 'txt':
            otv = str(otv).strip()
            pass

        case 'int':
            try:
                otv = int(otv)
            except:
                otv = Rezim_otveta(rezim_otveta)

        case 'float':
            try:
                if type(otv) == str:
                    otv = otv.replace(' ', '').replace(',', '.')
                otv = float(otv)
            except:
                otv = Rezim_otveta(rezim_otveta)

        case 'date':
            if type(otv) == str:
                otv = otv.replace(' ', '')

            try:
                otv = datetime.strptime(otv, date_format)
            except:
                otv = Rezim_otveta(rezim_otveta)

    return otv


def Arhiv_folder(folder_source_path, arhive_name):
    import py7zr

    with py7zr.SevenZipFile(arhive_name, 'w') as archive:
        archive.writeall(folder_source_path)
    pass
