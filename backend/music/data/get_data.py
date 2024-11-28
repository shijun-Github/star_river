# 导入数据请求模块
import requests
# 导入时间模块
import time
# 导入解密模块
import hashlib
# 导入正则表达式模块
import re
# 导入json模块
import json
# 导入制表模块
import prettytable as pt

# 模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 '
                  'Safari/537.36 Edg/119.0.0.0',
    'Cookie': 'kg_mid=3a8e2eda6b55afd434ed43d762bae621; kg_dfid=4XSJ8z0tMH343y3JOZ2ZluzO; '
              'kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1701158152,'
              '1701163020,1701180349,1701337969; kg_mid_temp=3a8e2eda6b55afd434ed43d762bae621; '
              'Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1701337996'
}


def Hash_md5(audio_id, date_time):
    # audio_id = '9gaecb60'
    s = [

        "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt",
        "appid=1014",
        # 时间戳
        f"clienttime={date_time}",
        "clientver=20000",
        "dfid=4XSJ8z0tMH343y3JOZ2ZluzO",
        # 歌曲id
        f"encode_album_audio_id={audio_id}",
        "mid=3a8e2eda6b55afd434ed43d762bae621",
        "platid=4",
        "srcappid=2919",
        "token=",
        "userid=0",
        "uuid=3a8e2eda6b55afd434ed43d762bae621",
        "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
    ]
    # 把列表拼接成字符串
    string = ''.join(s)
    MD5 = hashlib.md5()
    MD5.update(string.encode('utf-8'))
    signature = MD5.hexdigest()
    # print(signature)
    return signature


def search_MD5(world, date_time):
    search_s = [
        "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt",
        "appid=1014",
        "bitrate=0",
        "callback=callback123",
        f"clienttime={date_time}",
        "clientver=1000",
        "dfid=4XSJ8z0tMH343y3JOZ2ZluzO",
        "filter=10",
        "inputtype=0",
        "iscorrection=1",
        "isfuzzy=0",
        f"keyword={world}",
        "mid=3a8e2eda6b55afd434ed43d762bae621",
        "page=1",
        "pagesize=30",
        "platform=WebFilter",
        "privilege_filter=0",
        "srcappid=2919",
        "token=",
        "userid=0",
        "uuid=3a8e2eda6b55afd434ed43d762bae621",
        "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
    ]
    search_string = ''.join(search_s)
    MD5 = hashlib.md5()
    MD5.update(search_string.encode('utf-8'))
    search_signature = MD5.hexdigest()
    # print(signature)
    return search_signature


# audio_id = '9gaecb60'
# 获取当前时间的毫秒数
# 时间戳13位，所以是到毫秒的，所以我们要*1000，因为我们获取当前时间只精确到秒
date_time = int(time.time() * 1000)
# signature = Hash_md5(audio_id, date_time)


# key = '周杰伦'
key = input('请输入歌名或歌手：')
# 获取加密参数
search_signature = search_MD5(key, date_time)

# 搜索链接
search_url = 'https://complexsearch.kugou.com/v2/search/song?'
# 搜索请求参数
search_data = {
    'callback': 'callback123',
    'srcappid': '2919',
    'clientver': '1000',
    'clienttime': date_time,
    'mid': '3a8e2eda6b55afd434ed43d762bae621',
    'uuid': '3a8e2eda6b55afd434ed43d762bae621',
    'dfid': '4XSJ8z0tMH343y3JOZ2ZluzO',
    'keyword': key,
    'page': '1',
    'pagesize': '30',
    'bitrate': '0',
    'isfuzzy': '0',
    'inputtype': '0',
    'platform': 'WebFilter',
    'userid': '0',
    'iscorrection': '1',
    'privilege_filter': '0',
    'filter': '10',
    'token': '',
    'appid': '1014',
    'signature': search_signature
}

# 发送请求
response = requests.get(url=search_url, params=search_data, headers=headers)
"""" 获取数据 """
search_data = response.text
html_data = re.findall('callback123\((.*)', search_data)[0].replace(')', '')
# 把json字符串，转成字典数据
json_data = json.loads(html_data)
# print(json_data)
tb = pt.PrettyTable()
tb.field_names = ['序号', '歌名', '歌手', '专辑', 'id']
lis = []
num = 1
# for循坏遍历
for index in json_data['data']['lists']:
    dit = {
        '歌名': index['SongName'],
        '歌手': index['SingerName'],
        '专辑': index['AlbumName'],
        'id': index['EMixSongID']
    }
    lis.append(dit)
    tb.add_row([num, index['SongName'], index['SingerName'], index['AlbumName'], index['EMixSongID']])
    num += 1
    # print(dit)
    # print(audio_id)
print(tb)


# audio_id = input('请输入歌曲id：')
# signature = Hash_md5(audio_id, date_time)

def save(audio_id):
    signature = Hash_md5(audio_id, date_time)
    """" 发送请求 """
    # 请求链接
    url = 'https://wwwapi.kugou.com/play/songinfo?'
    # 请求参数
    data = {
        'srcappid': '2919',
        'clientver': '20000',
        'clienttime': date_time,
        'mid': '3a8e2eda6b55afd434ed43d762bae621',
        'uuid': '3a8e2eda6b55afd434ed43d762bae621',
        'dfid': '4XSJ8z0tMH343y3JOZ2ZluzO',
        'appid': '1014',
        'platid': '4',
        'encode_album_audio_id': audio_id,
        'token': '',
        'userid': '0',
        'signature': signature
    }
    # 发送请求
    response = requests.get(url=url, params=data, headers=headers)
    """" 获取数据 """
    json_data = response.json()
    print(json_data)
    """" 解析数据 """
    # 歌名
    audio_name = json_data['data']['audio_name']
    # 音频链接
    play_url = json_data['data']['play_url']
    # 歌词
    lyrics = json_data['data']['lyrics']
    # 匹配歌曲信息中的列表部分并替换为空字符串
    song_info_cleaned = re.sub("\[(.*?)\]", "", lyrics)
    # 图片
    img = json_data['data']['img']
    music_img = requests.get(url=img, headers=headers).content
    # print(img)
    print(audio_name, play_url)
    #
    # """
    #     保存数据
    #     图片/音频/视频/特定格式的文件 <获得链接>
    #     对于链接发送请求，获得二进制数据进行保存
    # """
    # print(audio_name, play_url)
    # 对于音频发送请求，获取二进制数据
    # music_content = requests.get(url=play_url, headers=headers).content
    # with open(audio_name + '.mp3', mode='wb+') as f:
    #     # 写入保存数据
    #     f.write(music_content)
    # # print(response.json())
    # print(f'{audio_name}.mp3下载完成')
    # print('下载完成')
    # # 歌词
    # with open(f'酷狗音乐\\{audio_name}.txt', 'w+', encoding="utf-8") as f:
    #     f.write(song_info_cleaned)
    # print(f'{audio_name}.txt下载完成')
    # # 图片
    # with open('酷狗音乐\\' + audio_name + '.jpg', mode='wb+') as f:
    #     # 写入保存数据
    #     f.write(music_img)
    # # print(response.json())
    # print(f'{audio_name}.jpg下载完成')


if __name__ == '__main__':
    # save(audio_id)
    page = input('请输入你要下载的歌曲序号 / 全部下载<0>:')
    try:
        if page == '0':
            for li in lis:
                save(audio_id=li['id'])
        else:
            save(audio_id=lis[int(page) - 1]['id'])
    except Exception as e:
        print('你可能输入有误', e)


