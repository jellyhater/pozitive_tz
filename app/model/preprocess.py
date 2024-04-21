import numpy as np
import pandas as pd


def preprocess_item(item):
    data = pd.Series(item)
    # initializing necessary variable features
    request_size = data["REQUEST_SIZE"]
    response_code = data['RESPONSE_CODE']
    client_useragent = data['CLIENT_USERAGENT'] if not is_none(data['CLIENT_USERAGENT']) else 'none'
    device = client_useragent.split()[0]
    # extracting features from request size
    data['NONE_REQUEST_SIZE'] = is_none(request_size)
    data['NORMAL_REQUEST_SIZE'] = int(request_size) < 6000 if str(request_size).isnumeric() else False
    data['LARGE_REQUEST_SIZE'] = int(request_size) >= 6000 if str(request_size).isnumeric() else False
    data['ANOMALY_REQUEST_SIZE'] = not str(request_size).isnumeric() and not is_none(request_size)
    # extracting features from response code
    data['NONE_RESPONSE_CODE'] = is_none(response_code)
    data['200s_RESPONSE_CODE'] = 200 <= int(response_code) < 300 if str(response_code).isnumeric() else False
    data['300s_RESPONSE_CODE'] = 300 <= int(response_code) < 400 if str(response_code).isnumeric() else False
    data['400s_RESPONSE_CODE'] = 400 <= int(response_code) < 500 if str(response_code).isnumeric() else False
    data['500s_RESPONSE_CODE'] = 500 <= int(response_code) < 600 if str(response_code).isnumeric() else False
    data['ANOMALY_RESPONSE_CODE'] = int(response_code) >= 600 or int(response_code) < 200 if str(
        response_code).isnumeric() else not is_none(response_code)
    # extracting features from matched variable src
    matched_variable_src_uniques = [
        'REQUEST_FILES',
        'REQUEST_CONTE',
        'RESPONSE_HEADERS',
        'REQUEST_ARGS_KEYS',
        'REQUEST_CONTENT_TYPE',
        'REQUEST_COOKIES',
        'REQUEST_POST_ARGS',
        'REQUEST_ARGS',
        'CLIENT_USERAGENT',
        'RESPONSE_BODY',
        'REQUEST_URI',
        'REQUEST_METHOD',
        'CLIENT_SESSION_ID',
        'CLIENT_IP',
        'REQUEST_QUERY',
        'REQUEST_JSON',
        'REQUEST_XML',
        'REQUEST_HEADERS',
        'REQUEST_HEADE',
        'REQUEST_PATH',
        'REQUEST_GET_ARGS'
    ]
    for value in matched_variable_src_uniques:
        data[value + '_MATCHED_VARIABLE_SRC'] = value in data['MATCHED_VARIABLE_SRC'] if not is_none(
            data['MATCHED_VARIABLE_SRC']) else False
    data['ANOMALY_MATCHED_VARIABLE_SRC'] = is_none(data['MATCHED_VARIABLE_SRC'])

    # extracting features from User-Agent
    data['LARGE_DEVICE'] = len(device) > 50
    data['SMALL_DEVICE'] = len(device) < 9
    data['NORMAL_DEVICE'] = (50 >= len(device) >= 9)
    data['LEN_USER_DEVICE_SPLIT_FLAG'] = len(client_useragent.split(' ')) > 4
    data['LINUX_FLAG'] = 'linux' in client_useragent.lower()
    data['WINDOWS_FLAG'] = 'windows' in client_useragent.lower()
    data['APPLE_DEVICE_FLAG'] = 'iphone' in client_useragent.lower() or 'ipad' in client_useragent.lower()
    # deleting features unnecessary for model
    del data['REQUEST_SIZE'], \
        data["MATCHED_VARIABLE_SRC"], \
        data['RESPONSE_CODE'], \
        data['CLIENT_USERAGENT'], \
        data['CLIENT_IP'], \
        data['MATCHED_VARIABLE_NAME'], \
        data['MATCHED_VARIABLE_VALUE'], \
        data['EVENT_ID']
    # return data in format suitable for scikit-learn classifiers
    return [data]


def is_none(value):
    for none_value in [None, np.nan, "None", "none", "nan", ""]:
        if value is none_value:
            return True
    return False