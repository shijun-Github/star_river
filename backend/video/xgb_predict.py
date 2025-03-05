import time
from pprint import pprint

import pandas as pd
import redis
import sys
import json

import xgboost as xgb
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from xgb_train import get_user_feature_by_user_id, get_item_feature_by_item_id, xgb_data_feature_concat_deal, \
    get_user_feature_batch_by_user_ids, get_item_feature_batch_by_item_ids, func_get_samples_feature_for_model

sys.path.append('..')  # 假设'..'是drama和utils的父目录

from utils.func_tablestore import get_data_from_tablestore_sql
from utils.config_constants import get_env_config


config = get_env_config('uat')
redis_dict = {'test': '1', 'uat': '1', 'prod': '1'}
mysql_dict = {'test': '1', 'uat': '1', 'prod': '2'}
redis_client = redis.StrictRedis(host=config['redis']['1']['host'],
                                 port=config['redis']['1']['port'],
                                 password=config['redis']['1']['password'])

# 获取预测数据
# 获取正负样本
day_1 = time.strftime("%Y-%m-%d", time.localtime(time.time() - 1*60*60*24))
day_2 = time.strftime("%Y-%m-%d", time.localtime(time.time() - 2*60*60*24))
day_3 = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3*60*60*24))
print(day_1, day_2, day_3)

user_info = get_data_from_tablestore_sql(f"""(
                    select *
                    from app_theatre_user_content_d_a_dt
                    where user_id REGEXP '[89]$' and length(click_id_list)>2 and report_date='{day_1}'
                    )""", config, "1")
user_info['expose_id_list'] = user_info[['expose_id_list']].apply(lambda row: [item['content_id'] for item in json.loads(row['expose_id_list'])], axis=1)
user_info['click_id_list'] = user_info[['click_id_list']].apply(lambda row: [item['content_id'] for item in json.loads(row['click_id_list'])], axis=1)
print(user_info)
demo = user_info[['user_id' ,'expose_id_list', 'click_id_list']].head(1).to_dict()
print(demo, type(demo))



def xbg_predict_http(user_id_in, item_ids_in):
    """
    模型预测接口
    user_id_in: 1044789836037490698
    item_ids_in: ['115', '212', '3']
    """
    # print(user_id_in, item_ids_in)
    # user_ids, item_ids 推荐接口输入这两个参数
    t_s = time.time()
    req = pd.DataFrame({'user_id': [user_id_in]*len(item_ids_in),
                        'item_id': item_ids_in})
    print(req)
    # 将数据拼接处理为模型需要的格式
    feature_df = func_get_samples_feature_for_model(req, day_2, config)
    # print(feature_df)
    # 将数据转为xgb的
    dtest = xgb.DMatrix(feature_df)
    # 加载模型
    loaded_model = xgb.Booster()
    loaded_model.load_model('model_file/xbg_model.model')
    # 使用加载的模型进行预测
    y_pred = loaded_model.predict(dtest)
    res = {'data':{
        'user_id': user_id_in,
        'item_id': item_ids_in,
        'score': y_pred.tolist()
    }}
    pprint(res)
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ cost time: ', len(item_ids_in), time.time() - t_s)



for index, row in user_info.iterrows():
    user_id = row['user_id']
    item_ids = list(set(row['expose_id_list']))
    item_ids_click = list(set(row['click_id_list']))
    print(user_id, item_ids, item_ids_click)
    xbg_predict_http(user_id, item_ids)
    time.sleep(1)
    print()




# print(roc_auc_score(label_df, y_pred))
# y, pred = label_df, pd.DataFrame(y_pred, columns=['pred'])
# res = pd.concat([y.reset_index(drop=True), pred.reset_index(drop=True)], axis=1)
# print(res.sort_values(by='pred', ascending=False))
# # print(res.head(60))
#
#
#
# ###############
#
# feature_list = []
# label_list = []
#
# feature_list.append(user_feature + item_feature)  # 合并用户特征和视频特征
# label_list.append(label)
#
# feature_df_in = pd.DataFrame(feature_list)
# label_df_in = pd.DataFrame(label_list)
# feature_df_in = feature_df_in.astype('float32')
# label_df_in = label_df_in.astype('float32')
# return feature_df_in, label_df_in
# ##############
#
#
#
#
# def func_xgp_predict(user_id, item_ids):
#     """ 针对召回进行排序 """
#     user_info = pd.DataFrame({'user_id': user_id,'item_ids': [item_ids]},
#                              columns=['user_id', 'item_ids'])
#     print(user_info)
#     # 将数据拼接处理为模型需要的格式
#     feature_df, label_df = xgb_data_feature_concat_deal(user_info, day_2, config)
#     print(feature_df)
#     print(label_df)
#     # 将数据转为xgb的
#     dtest = xgb.DMatrix(feature_df, label_df)
#     # 使用加载的模型进行预测
#     y_pred = loaded_model.predict(dtest)
#     print(roc_auc_score(label_df, y_pred))
#     y, pred = label_df, pd.DataFrame(y_pred, columns=['pred'])
#     res = pd.concat([y.reset_index(drop=True), pred.reset_index(drop=True)], axis=1)
#     print(res.sort_values(by='pred', ascending=False))
#
# user_id = '1044789836037490698'
# item_ids = ['115', '212', '3']
# print('(((((9999999999999999999999999999999999999')
# func_xgp_predict(user_id, item_ids)