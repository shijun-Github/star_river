# 下载
import os
import re

import requests


def download(url, path, name):
    res = requests.get(url)
    suffix = re.findall('(jpg|png)', url)[0]
    way = path + os.sep + name + '.' + suffix
    with open(way, 'ab') as file:
        file.write(res.content)
        file.flush()
    return way


def downloadMusic(url, path, name, suffix='mp3'):
    res = requests.get(url)
    way = path + os.sep + name + '.' + suffix
    with open(way, 'ab') as file:
        file.write(res.content)
        file.flush()
    return way
