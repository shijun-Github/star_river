# -*- coding: utf-8 -*-

import os
from pprint import pprint

import pandas as pd
import requests
import json
import time
import random
from backend.utils.product_sign import get_sign_jd_dataoke

pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列


def func_get_goods_info_jd():
    """
    获取数据,并获取格式化数据为前端可用的格式
    """
    path_data = os.getcwd().split('backend')[0] + 'backend\goods\data\jd_goods_info.csv'
    # path_data = os.getcwd() +  '\data\jd_goods_info.csv'
    os.remove(path_data)
    # 旧数据
    # old_data = pd.read_csv(path_data)[['item_id']]
    eliteId_list = [130, 1, 2, 10, 22, 23, 25, 31, 32, 40, 41, 112, 129, 153, 12318]  # 取哪些频道的数据
    eliteId_list = [130, 1]  # 取哪些频道的数据
    for eliteId in eliteId_list:
        page_index_num = 20  # 多少页
        pageSize = 20  # 一页多少条
        for pageIndex in range(1, page_index_num):
            try:
                # 获取某个频道的某页数据
                url_ = 'https://openapiv2.dataoke.com/open-api/jd-jingfen-goods'
                parameters = {
                    # 系统参数
                    'appKey': '65b0bc2864fba',
                    'appSecret': '2ae8b46c6b3655819cbc1ceab81341d1',  # secretkey
                    'version': 'v1.0.0',
                    # 业务参数
                    'eliteId': eliteId,
                    'pageIndex': pageIndex,
                    'pageSize': pageSize,
                }
                parameters['signRan'] = get_sign_jd_dataoke(params=parameters)  # 生成签名
                t = requests.get(url=url_, params=parameters, headers={'content-Type': 'application/json'})
                tt = t.json()
                print(eliteId, pageIndex, '=========', tt.get('msg', True), tt)
                if tt.get('msg', '成功') != "成功":
                    break
                # 每页存一次数据
                value_batch = []
                for item_info_ori in tt['data']['list']:
                    try:
                        need_feature = {
                            # 公共参数（商品、视频、音乐）
                            'item_id': item_info_ori['skuId'],
                            'item_name': item_info_ori['skuName'],
                            'author_name': item_info_ori['shopInfo']['shopName'],
                            'cover_url': item_info_ori['imageInfo']['imageList'][0]['url'],
                            # 商品参数
                            'extend': json.dumps([
                                '原价:' + str(item_info_ori['priceInfo']['price']),
                                # 如果没有优惠券，这条数据就不要了
                                '券额:' + str([cp['discount'] for cp in item_info_ori['couponInfo']['couponList'] if cp['isBest'] == 1][0]),
                                '券后:' + str(item_info_ori['priceInfo']['lowestCouponPrice']),
                                '评分:' + str(item_info_ori['commissionInfo']['couponCommission']),
                            ]),
                        }
                        value_batch.append(need_feature)
                    except Exception as ex:
                        print('single need_feature error: ', ex)
                value_batch_df = pd.DataFrame.from_records(value_batch)
                header_flag = False if path_data.split('\\')[-1] in os.listdir(path_data.split(path_data.split('\\')[-1])[0]) else True
                value_batch_df.to_csv(path_data, mode='a', header=header_flag, index=False)
            except Exception as ex:
                print('except Exception as ex: ', ex)
            time.sleep(random.randint(3, 10))


if __name__ == '__main__':
    """
    """
    print("扛起达到向前冲！！！")
    func_get_goods_info_jd()

