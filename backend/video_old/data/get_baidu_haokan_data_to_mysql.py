from pprint import pprint

import numpy as np
import pymysql
import time
import datetime
import pandas as pd
import os
import json
import random
import requests
from sqlalchemy import create_engine
from backend.utils import func_mysql
pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列


def get_baidu_haokan_video():
    # 第一步：数据的抓取
    # 定义一个变量，用于存取爬取到的数据
    # 反反爬
    headers = {
        # User-Agent
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        # Referer 用于判断你是从哪个页面跳过来的
        'referer': 'https://haokan.baidu.com/?fr=pc_pz',
        # Cookie 用于判断是否你登录（如果没有登录，是没有cookie的）
        'cookie': 'BIDUPSID=05FEFAC34AEB974EB63623DBB54F3765; PSTM=1590673047; __yjs_duid=1_223b526dd2e6b4ea4aa28b6a28e3398a1618362899184; BAIDUID=05FEFAC34AEB974EF3880088E7AC8536:SL=0:NR=10:FG=1; BAIDUID_BFESS=05FEFAC34AEB974EF3880088E7AC8536:SL=0:NR=10:FG=1; BDRCVFR[w-kNo__JL0t]=1jmUUpB1KcCmh7GmLNEmi4WUvY; delPer=0; PSINO=1; H_PS_PSSID=34099_31253_33848_33607_34094_26350; BA_HECTOR=a1aha4052hakah804b1gcbeil0q; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[fb3VbsUruOn]=rJZwba6_rOCfAF9pywd; BCLID=11157415508952475120; BDSFRCVID=YiuOJexroG38bzJevE5BMBPcTOqMFyTTDYLEJs2qYShnrsPVJeC6EG0PtoWQkz--EHtdogKKBmOTHgKF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR3aQ5rtKRTffjrnhPF3KhDfXP6-hnjy3bAO3tFa54QpHRcELl3j3M4LXtj8Lp3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJaavIB-FEHl51fbbvbURvL4ug3-7MBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoCvt-5rDHJTg5DTjhPrM3RjdWMT-MTryKK8yKtFhetQHjf5YLl8S3-nDWx58QNnRhlR2B-3iV-OxDUvnyxAZyxomtfQxtNRJWM3l2-FVKq5S5-OobUPULxc9LUvMW2cdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtCvsHJ7c-tI_-4_tbh_X5-RLfa50Ll7F54nKDp0Re-50y4LBQHoGWxjTKan9Ql6IMxbxsMTsQf65DR_40U7XbJJTQeQ-5KQN3KJmfb750tR0qDukyhOb2-biW2rL2Mbd5hvP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe4bK-TrXDauHtx5; BCLID_BFESS=11157415508952475120; BDSFRCVID_BFESS=YiuOJexroG38bzJevE5BMBPcTOqMFyTTDYLEJs2qYShnrsPVJeC6EG0PtoWQkz--EHtdogKKBmOTHgKF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tR3aQ5rtKRTffjrnhPF3KhDfXP6-hnjy3bAO3tFa54QpHRcELl3j3M4LXtj8Lp3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJaavIB-FEHl51fbbvbURvL4ug3-7MBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoCvt-5rDHJTg5DTjhPrM3RjdWMT-MTryKK8yKtFhetQHjf5YLl8S3-nDWx58QNnRhlR2B-3iV-OxDUvnyxAZyxomtfQxtNRJWM3l2-FVKq5S5-OobUPULxc9LUvMW2cdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtCvsHJ7c-tI_-4_tbh_X5-RLfa50Ll7F54nKDp0Re-50y4LBQHoGWxjTKan9Ql6IMxbxsMTsQf65DR_40U7XbJJTQeQ-5KQN3KJmfb750tR0qDukyhOb2-biW2rL2Mbd5hvP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe4bK-TrXDauHtx5; BDUSS=EgtYkpkdHRPRmNHSE9hTUlXdzZSTEo2N1FvUzFFd1JrTXVzYXV6N0VYQU9UZTFnRUFBQUFBJCQAAAAAAQAAAAEAAAAP3ewBc25vd2xpZmVzcwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA7AxWAOwMVga; BDUSS_BFESS=EgtYkpkdHRPRmNHSE9hTUlXdzZSTEo2N1FvUzFFd1JrTXVzYXV6N0VYQU9UZTFnRUFBQUFBJCQAAAAAAQAAAAEAAAAP3ewBc25vd2xpZmVzcwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA7AxWAOwMVga; Hm_lvt_4aadd610dfd2f5972f1efee2653a2bc5=1623571282,1623571295,1623572498; Hm_lpvt_4aadd610dfd2f5972f1efee2653a2bc5=1623572498; ab_sr=1.0.1_N2JmMjdkMDQ4YjhmOTZjNzY0MWFhZDU4ODU0ZDQ2NzgzZDAxODZmMWVkNGNmYWNjYTIxMjY0NGYzMWU5ZDA0MDZlNmVmODBlOWJkZGE3M2M1YTllYzA1MGVkMTQ2OTRkMDYwMTI2OThmYTJmMDEyZjk0ZjY0MjY4YjhlNmE3ZTUxNDU2MDMzNGIyNzQ2ZmFkZDM4ODVmYmQ5ZTcxNTFkMg==; reptileData=%7B%22data%22%3A%22b63c3c44ce7bc20eda633b56a7a8001dd67cef3dba2333c93cda863c2fdf2fb5d9e24be71639bdeb4dc0343566aef2c9e23a0318e7b5031322b35e380f87464fbd2c17a9a1ced8623fca3edcebaffd6a6b0b671f5faf3dfe9a56f8c9f7e0c6550289a890ebc252822d02af6411c79d729c53e4334fa15b6100077783e37fade1%22%2C%22key_id%22%3A%2230%22%2C%22sign%22%3A%22f18c8fe9%22%7D'
    }

    def get_data(tab_, page_index_):
        base_url = f'https://haokan.baidu.com/web/video/feed?tab={tab_}&act=pcFeed&pd=pc&page={page_index_}&num=20&shuaxin_id=1623571294796'
        # 第二步：取出数据
        # 使用request的get 请求，把数据拿出来
        response = requests.get(base_url, headers=headers)  # 第一次请求
        # print(response.status_code)  # 打印出来的结果是200，否则爬取数据失败
        # 把爬到的数据用json格式显示
        data = response.text  # 文本格式（json）
        # print(data)  # 打印出来的结果与Request URL中链接结果的json数据相同
        # 第三步：json格式的数据解析
        # json.loads -- 将json编码的字符串转换为一个python数据结构
        # json.dump -- 将python数据结构转换为json
        json_data = json.loads(data)
        # 有顺序的放入嵌套结构中的key值
        json_list = json_data['data']['response']['videos']
        tmp_df = pd.DataFrame(json_list)
        print(tmp_df)
        if tmp_df.shape[0] > 0:
            print(tmp_df.shape[0], "================")
            tmp_df['playcnt'] = tmp_df['playcnt'].astype("int")
            tmp_df = tmp_df[tmp_df['playcnt']>0]
            tmp_df['publish_time'] = tmp_df['playcnt'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + float(x))))
        return tmp_df

    page_num = 3
    channel_list = ['yingshi_new', 'yunying_vlog', 'yunying_vlog', 'youxi_new']
    for tab in channel_list:
        for page_index in range(page_num):
            data_df = get_data(tab, page_index)
            data_df['channel'] = tab
            print(data_df)
            pprint(data_df.head(1).to_dict(orient='records'))

            # func_mysql.func_insert_data_into_mysql_table_df_tosql(data_df=data_df, database='video', table_name='video_baidu_haokan')
            time.sleep(random.randint(3, 10))


if __name__ == '__main__':
    print("扛起大刀。。。")
    get_baidu_haokan_video()






