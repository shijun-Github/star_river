import time
from os import times
from pprint import pprint

import requests

# from backend.music.codes_test import play_url


def get_playlist():
    """
    获取所有歌单
    """
    res = []
    for i in range(2):
        page_index, page_size = i, 3
        url_ = 'http://music.163.com/api/playlist/list?limit=%s&offset=%s' % (page_size, page_index*page_size)
        rep = requests.get(url=url_, headers={'Content-Type': 'application/json'})
        rep = rep.json()['playlists']
        # rep = [item['id'] for item in rep]
        # pprint(rep)
        print(len(rep), rep)
        res.extend(rep)
    return res


def get_playlist_song(playlist_id):
    """
    获取歌单内的歌曲 ， 内部可以获取到歌曲需要的各种信息
    12696691965 12218945872
    https://music.163.com/api/playlist/detail?id=3778678
     """
    # playlist_id = ['12696691965', '12636330404', '12218945872']
    # playlist_id = '12636330404'
    # playlist_name = '前奏沦陷 | 首尔的风吹不散浪漫'
    ids = playlist_id
    url_ = 'http://music.163.com/api/playlist/detail?id=%s' % ids
    rep = requests.get(url=url_, headers={'Content-Type': 'application/json'})
    print(rep.json())
    rep = rep.json()['result']
    rep = rep['tracks']
    pprint(rep)
    # print(len(rep), rep)
    # pprint(rep[0])
    for song_info in rep:
        tmp = {
            'song_name': song_info['name'],
            'song_name_trans': song_info['transName'],
            'alias': song_info['alias'],
            'duration': song_info['duration'],
            # 'song_tags': song_info['tags'],
            'singer_name':', '.join([item['name'] for item in song_info['artists']]),
            'song_cover': song_info['album']['picUrl'],
            # 'song_createTime': song_info['createTime'],
            'song_mp3_url': 'https://music.163.com/song/media/outer/url?id=%s.mp3' % song_info['id'],
        }
        print(song_info)
        print(tmp)


def get_song_info(song_id):
    """

    :return:  1364586007   12636330404
    https://music.163.com/song/media/outer/url?id=12278356.mp3
    """
    # play_url = 'https://music.163.com/song/media/outer/url?id=%s.mp3' % song_id
    # print(play_url)
    rep = requests.get(url="http://music.163.com/api/song/detail/?id=" + str(song_id) + "&ids=[" + str(song_id) + "]",
                       headers={'Content-Type': 'application/json'})
    rep = rep.json()
    pprint(rep)
    print(rep)
    print(rep[''])

    # rep = requests.post(url='http://music.163.com/weapi/v3/song/detail/?id=' + str(song_id) + "&ids=[" + str(song_id) + "]",
    #                    headers={'Content-Type': 'application/json'})
    # print('=====', rep)
    # print(rep.json())


if __name__ == '__main__':
    """
    这里可以获取歌单和歌单里面歌曲的各种信息。可以直接使用
    但是目前会员歌曲无法用
    """
    playlists = get_playlist()
    print(len(playlists), playlists)
    # playlist_id = playlists[0]['id']
    # print(playlist_id)
    # get_playlist_song(playlist_id)
    # get_song_info('26096272')