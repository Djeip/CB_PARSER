import zipfile
import os
import time

import xmltodict
import requests
import shutil
import pandas as pd


def unzip(path_to_zip_file, file_name, directory_to_extract_to):
    """Разархивация файла"""
    with zipfile.ZipFile(path_to_zip_file + file_name, 'r') as zip_ref:
        for name in zip_ref.namelist():
            zip_ref.extract(name, directory_to_extract_to)
    shutil.rmtree(path_to_zip_file)


# noinspection PyPep8Naming
def table_parse(tbl):
    try:
        name = tbl['ParticipantInfo']['@NameP']
    except KeyError:
        name = None
    try:
        BIC = tbl['@BIC']
    except KeyError:
        BIC = None
    try:
        PrntBIC = tbl['ParticipantInfo']['@PrntBIC']
    except KeyError:
        PrntBIC = None
    try:
        PTtype = tbl['ParticipantInfo']['@PtType']
    except KeyError:
        PTtype = None
    try:
        OKATO = tbl['ParticipantInfo']['@Rgn']
    except KeyError:
        OKATO = None
    try:
        INDEX = tbl['ParticipantInfo']['@Ind']
    except KeyError:
        INDEX = None
    try:
        CNTRCD = tbl['ParticipantInfo']['@CntrCd']
    except KeyError:
        CNTRCD = None
    try:
        TNP = tbl['ParticipantInfo']['@Tnp']
    except KeyError:
        TNP = None
    try:
        NNP = tbl['ParticipantInfo']['@Nnp']
    except KeyError:
        NNP = None
    try:
        ADR = tbl['ParticipantInfo']['@Adr']
    except KeyError:
        ADR = None
    try:
        DATEIN = tbl['ParticipantInfo']['@DateIn']
    except KeyError:
        DATEIN = None
    try:
        SRVCS = tbl['ParticipantInfo']['@Srvcs']
    except KeyError:
        SRVCS = None
    try:
        XCHTYPE = tbl['ParticipantInfo']['@XchType']
    except KeyError:
        XCHTYPE = None
    try:
        ACCOUNT = tbl['Accounts'][0]['@Account']
    except KeyError:
        ACCOUNT = None
    try:
        REGULATIONACCOUNTTYPE = tbl['Accounts'][0]['@RegulationAccountType']
    except KeyError:
        REGULATIONACCOUNTTYPE = None
    try:
        CK = tbl['Accounts'][0]['@CK']
    except KeyError:
        CK = None
    try:
        ACCOUNTCBRBIC = tbl['Accounts'][0]['@AccountCBRBIC']
    except KeyError:
        ACCOUNTCBRBIC = None
    try:
        ACCOUNTDATEIN = tbl['Accounts'][0]['@DateIn']
    except KeyError:
        ACCOUNTDATEIN = None
    try:
        ACCOUNTSTATUS = tbl['Accounts'][0]['@AccountStatus']
    except KeyError:
        ACCOUNTSTATUS = None
    return {
        'BANK': name,
        'BIC': BIC,
        'PRNT_BIC': PrntBIC,
        'PT_TYPE': PTtype,
        'OKATO': OKATO,
        'POCHT_INDEX': INDEX,
        'CNTRCD': CNTRCD,
        'TNP': TNP,
        'NNP': NNP,
        'ADR': ADR,
        'DATEIN': DATEIN,
        'SRVCS': SRVCS,
        'XCHTYPE': XCHTYPE,
        'ACCOUNT': ACCOUNT,
        'REGULATIONACCOUNTTYPE': REGULATIONACCOUNTTYPE,
        'CK': CK,
        'ACCOUNTCBRBIC': ACCOUNTCBRBIC,
        'ACCOUNTDATEIN': ACCOUNTDATEIN,
        'ACCOUNTSTATUS': ACCOUNTSTATUS

    }


def xml_finder(dir):
    return [_ for _ in dir if _.endswith(r'.xml')]


def SPR_BIC():
    DIR_PATH = time.strftime('%Y_%m_%d')
    URL = 'https://cbr.ru/s/newbik'

    FILE_NAME = "T_SPR_BIC.zip"

    nm = """C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/INPUT/""" + DIR_PATH + """_d/"""

    if not os.path.isdir(nm):
        os.mkdir(nm)

    nm_out = """C:/Users/Администратор/Documents/GitHub/POTENCIAL_DE_PARSING/INPUT/""" + DIR_PATH

    resp = requests.get(URL)
    with open(nm + FILE_NAME, 'wb') as f:
        f.write(resp.content)

    unzip(nm, FILE_NAME, nm_out)

    with open(nm_out + "/" + xml_finder(os.listdir(nm_out))[0], "r") as f:  # opening xml file
        content = f.read()

    tmp = xmltodict.parse(content)['ED807']['BICDirectoryEntry']

    df = pd.DataFrame(list(map(table_parse, tmp)))
    return df
