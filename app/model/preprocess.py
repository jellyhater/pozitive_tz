import numpy as np
import pandas as pd
from numbers import Number
from copy import deepcopy


def preprocess_item(item):
    json_data = deepcopy(item)
    # initializing necessary variable features
    request_size = json_data["REQUEST_SIZE"]
    response_code = json_data['RESPONSE_CODE']
    client_useragent = json_data['CLIENT_USERAGENT'] if json_data['CLIENT_USERAGENT'] else 'none'
    device = client_useragent.split()[0]
    # extracting features from request size
    json_data['NONE_REQUEST_SIZE'] = request_size is np.nan
    json_data['NORMAL_REQUEST_SIZE'] = int(request_size) < 6000 if isinstance(request_size, Number) else False
    json_data['LARGE_REQUEST_SIZE'] = int(request_size) >= 6000 if isinstance(request_size, Number) else False
    json_data['ANOMALY_REQUEST_SIZE'] = not isinstance(request_size, Number)
    # extracting features from response code
    json_data['NONE_RESPONSE_CODE'] = response_code is np.nan
    json_data['200s_RESPONSE_CODE'] = 200 <= int(response_code) < 300 if isinstance(response_code, Number) else False
    json_data['300s_RESPONSE_CODE'] = 300 <= int(response_code) < 400 if isinstance(response_code, Number) else False
    json_data['400s_RESPONSE_CODE'] = 400 <= int(response_code) < 500 if isinstance(response_code, Number) else False
    json_data['500s_RESPONSE_CODE'] = 500 <= int(response_code) < 600 if isinstance(response_code, Number) else False
    json_data['ANOMALY_RESPONSE_CODE'] = int(response_code) >= 600 if isinstance(response_code, Number) else True
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
        json_data[value + '_MATCHED_VARIABLE_SRC'] = json_data['MATCHED_VARIABLE_SRC'] == value
    json_data['ANOMALY_MATCHED_VARIABLE_SRC'] = bool(json_data['MATCHED_VARIABLE_SRC'])
    # extracting features from User-Agent
    json_data['LARGE_DEVICE'] = len(device) > 50
    json_data['SMALL_DEVICE'] = len(device) < 9
    json_data['NORMAL_DEVICE'] = (50 >= len(device) >= 9)
    json_data['LEN_USER_DEVICE_SPLIT_FLAG'] = len(client_useragent.split(' ')) > 4
    json_data['LINUX_FLAG'] = 'linux' in client_useragent.lower()
    json_data['WINDOWS_FLAG'] = 'windows' in client_useragent.lower()
    json_data['APPLE_DEVICE_FLAG'] = 'iphone' in client_useragent.lower() or 'ipad' in client_useragent.lower()
    # deleting features unnecessary for model
    del json_data['REQUEST_SIZE'], \
        json_data["MATCHED_VARIABLE_SRC"], \
        json_data['RESPONSE_CODE'], \
        json_data['CLIENT_USERAGENT'], \
        json_data['CLIENT_IP'], \
        json_data['MATCHED_VARIABLE_NAME'], \
        json_data['MATCHED_VARIABLE_VALUE'], \
        json_data['EVENT_ID']
    # return data in format suitable for scikit-learn classifiers
    return [pd.Series(json_data)]
