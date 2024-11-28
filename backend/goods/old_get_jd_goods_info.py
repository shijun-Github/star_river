import pandas as pd
import requests
import json
import time
import random

from backend.utils.func_mysql import func_create_mysql_table, func_delete_mysql_table, \
    func_insert_data_into_mysql_table, func_get_data_from_mysql
from backend.utils.product_sign import get_sign_jd_dataoke


def func_deal_mysql_table():
    """
    这里主要是处理mysql表格
        1、删除表
        2、创建表
    """
    # 删除mysql表格
    # sql_delete = "DROP TABLE IF EXISTS goods.jd_goods_info_ori"
    # func_delete_mysql_table(sql_delete)
    # 创建mysql表格
    sql_create = """
        CREATE TABLE IF NOT EXISTS goods.jd_goods_info_ori (
           item_id VARCHAR(50) NOT NULL DEFAULT '0',
           info TEXT,
           status VARCHAR(50) NOT NULL DEFAULT '0',
           PRIMARY KEY (item_id)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8
            """
    func_create_mysql_table(sql_create)


def get_goods_info_jd():
    """
    获取数据
    """
    eliteId_list = [130, 1, 2, 10, 22, 23, 25, 31, 32, 40, 41, 112, 129, 153, 12318]  # 取哪些频道的数据
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
                
                # 将数据存储到MySQL中
                value_batch = []
                for item in tt['data']['list']:
                    value_batch.append(str((item['skuId'], json.dumps(item, ensure_ascii=False), '1')))
                value_batch = ','.join(value_batch)
                if len(value_batch) > 0:
                    sql_ = """
                            REPLACE INTO goods.jd_goods_info_ori(item_id, info, status)
                            VALUES %s
                            """ % value_batch
                    func_insert_data_into_mysql_table(sql_)
            except Exception as ex:
                print('except Exception as ex: ', ex)
            time.sleep(random.randint(3, 10))



def deal_goods_info_jd():
    """
    处理数据为前端可以直接使用的格式
    """
    goods_info_ori = func_get_data_from_mysql("""
                    select *
                    from goods.jd_goods_info_ori
                    """)
    print(goods_info_ori)
    res = []
    for index, row in goods_info_ori.iterrows():
        item_info_ori = json.loads(row['info'])
        tmp = {
            # 公共的字段
            'item_type': 'goods',  # goods/video/music
            'item_id': item_info_ori['skuId'],  # 物品id
            'item_name': item_info_ori['skuName'], # 物品名称（商品名称、歌曲名）
            'cover_image': item_info_ori['imageInfo']['imageList'][0],  # 封面
            'author_name': item_info_ori['shopInfo']['shopName'],  # 作者（店铺名、演唱者）
            # 商品场景
            'goods_extend':{
                'ori_price': item_info_ori['priceInfo']['price'],
                'real_price': item_info_ori['priceInfo']['lowestCouponPrice'],
                'score': item_info_ori['commissionInfo']['couponCommission'],
                'super_url': item_info_ori['materialUrl'],
            },
            # 音乐场景
            'music_extend': {
                'play_url': ''
            }
        }
        print(item_info_ori['skuId'], tmp)



if __name__ == '__main__':
    """
    """
    print("扛起达到向前冲！！！")
    get_goods_info_jd()
    # deal_goods_info_jd()

