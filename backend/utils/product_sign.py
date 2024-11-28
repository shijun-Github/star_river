import hashlib
import json
import time
import datetime
import pandas as pd
import requests
import random


# 取sign签名
def get_pdd_sign(params):
    client_secret = '1833b600ad4b6f03bebbad4a704e217dba3430b0'
    tt = client_secret + ''.join([k + str(v) for k, v in sorted(params.items())]) + client_secret
    sign = hashlib.md5(tt.encode('utf-8')).hexdigest().upper()
    return sign


# 取sign签名
def get_jd_sign(params):
    secret = 'd5501a870f9844aab8fde31cf35124cf'  # secretkey
    tt = secret + ''.join([k + str(v) for k, v in sorted(params.items())]) + secret
    sign = hashlib.md5(tt.encode('utf-8')).hexdigest().upper()
    return sign


def get_sign_jd_dataoke(params):
    """
    获取大淘客 京东 sign
    """
    params['nonce'] = str(random.randint(100000, 900000))
    params['timer'] = str(int(time.time()*1000))
    sign_ori = ('appKey=' + params['appKey'] + '&timer=' + params['timer'] + '&nonce=' + params['nonce'] +
                '&key=' + params['appSecret']).encode()
    sign = hashlib.md5(sign_ori).hexdigest().upper()
    return sign


