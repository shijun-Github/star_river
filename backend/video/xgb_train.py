import json
import random
import time
from pprint import pprint

import pandas as pd
import redis
import sys

import xgboost as xgb
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
sys.path.append('..')  # 假设'..'是drama和utils的父目录

from utils.func_tablestore import get_data_from_tablestore_sql, get_data_from_tablestore_sql_all_split_batch
from utils.config_constants import get_env_config


def get_item_feature_by_item_id(item_id, day, config):
    """ 通过物品id获取物品的模型特征 """
    item_info = get_data_from_tablestore_sql(f"""(
                        select *
                        from app_recommend_gameplay_features_event_date_d_inc_dt
                        where item_id='{item_id}' and report_date='{day}'
                        )""", config, "1")
    if item_info.empty:
        return False
    item_info['f_statistic'] = item_info.apply(lambda row: [row['expose_num'], row['click_num'], row['duration'], row['click_rate'], row['duration_rate']], axis=1)
    feature_vec = item_info[['f_statistic']].to_dict('records')[0]['f_statistic']
    return feature_vec

def get_item_feature_batch_by_item_ids(item_ids, day, config):
    """ 批量获取物品特征 """
    item_ids = '(' +  ','.join(["'" + str(item) + "'" for item in item_ids]) + ')'
    sql_ = f"""(
            select *
            from app_recommend_gameplay_features_event_date_d_inc_dt
            where item_id in {item_ids} and report_date='{day}'
            )"""
    item_info = get_data_from_tablestore_sql(sql_, config, "1")
    item_info['f_statistic'] = item_info.apply(lambda row: [row['expose_num'], row['click_num'], row['duration'], row['click_rate'], row['duration_rate']], axis=1)
    feature_vec_dict = item_info[['item_id', 'f_statistic']].set_index('item_id')['f_statistic'].to_dict()
    return feature_vec_dict

def get_user_feature_by_user_id(user_id, day, config):
    """ 通过用户id获取用户的模型特征 """
    user_info = get_data_from_tablestore_sql(f"""(
                        select *
                        from app_theatre_user_content_d_a_dt
                        where user_id='{user_id}' and report_date='{day}'
                        )""", config, "1")
    if user_info.empty:
        return False
    user_info['age'] = user_info[['age']].apply(lambda row:row['age'] if row['age'] is not None else 0, axis=1)
    user_info['sex'] = user_info[['sex']].apply(lambda row:row['sex'] if row['sex'] is not None else 0, axis=1)
    user_info['user_feature'] = user_info.apply(lambda row: [row['age'], row['sex']], axis=1)
    feature_vec = user_info[['user_feature']].to_dict('records')[0]['user_feature']
    return feature_vec


def get_user_feature_batch_by_user_ids(item_ids, day, config):
    """ 批量获取物品特征 """
    item_ids = '(' +  ','.join(["'" + str(item) + "'" for item in item_ids]) + ')'
    sql_ = f"""(
            select *
            from app_theatre_user_content_d_a_dt
            where user_id in {item_ids} and report_date='{day}'
            )"""
    user_info = get_data_from_tablestore_sql(sql_, config, "1")
    if user_info.empty:
        return {}
    user_info['age'] = user_info[['age']].apply(lambda row:row['age'] if row['age'] is not None else 0, axis=1)
    user_info['sex'] = user_info[['sex']].apply(lambda row:row['sex'] if row['sex'] is not None else 0, axis=1)
    user_info['user_feature'] = user_info.apply(lambda row: [row['age'], row['sex']], axis=1)
    # feature_vec = user_info[['user_feature']].to_dict('records')[0]['user_feature']
    feature_vec_dict = user_info[['user_id', 'user_feature']].set_index('user_id')['user_feature'].to_dict()
    return feature_vec_dict


def xgb_data_feature_concat_deal(user_info, day_feature, config):
    """
    user_id|item_id|label
    为正负样本获取特征并拼接好
    """
    feature_list = []
    label_list = []
    for index, row in user_info.iterrows():
        # 对于没有点击的用户，这种用户任务是无效用户，直接无视他的样本
        if len(row['click_id_list']) == 0:
            continue
        user_id = row['user_id']
        expose_id_list = list(set(row['expose_id_list']))
        click_id_list = list(set(row['click_id_list']))
        print("expose_id_list: ", expose_id_list)
        print("click_id_list: ", click_id_list)
        user_feature = get_user_feature_by_user_id(user_id, day_feature, config)
        # 并发获取item_id
        items_feature_dict = get_item_feature_batch_by_item_ids(list(set(expose_id_list + click_id_list)), day_feature, config)
        for item_id in expose_id_list:
            try:
                # 获取单个item_id的特征
                # item_feature = get_item_feature_by_item_id(item_id, day_feature, config)
                item_feature = items_feature_dict[item_id]
                if not item_feature:
                    continue
                label = 1 if item_id in click_id_list else 0
                print("+++++++++", user_id, item_id, user_feature, item_feature, user_feature+item_feature, label)
                feature_list.append(user_feature + item_feature)  # 合并用户特征和视频特征
                label_list.append(label)
            except Exception as e:
                print('for item_id in expose_id_list:', e)
    feature_df_in = pd.DataFrame(feature_list)
    label_df_in = pd.DataFrame(label_list)
    feature_df_in = feature_df_in.astype('float32')
    label_df_in = label_df_in.astype('float32')
    return feature_df_in, label_df_in


def get_pn_samples(day):
    """ 获取正负样本 """
    user_info = get_data_from_tablestore_sql(f"""(
                        select *
                        from app_theatre_user_content_d_a_dt
                        where user_id REGEXP '[12345]$' and report_date='{day}'
                        limit 30
                        )""", config, "1")
    user_info['expose_id_list'] = user_info[['expose_id_list']].apply(
        lambda row: [item['content_id'] for item in json.loads(row['expose_id_list'])], axis=1)
    user_info['click_id_list'] = user_info[['click_id_list']].apply(
        lambda row: [item['content_id'] for item in json.loads(row['click_id_list'])], axis=1)
    print(user_info)
    sample_list = []
    for index, row in user_info.iterrows():
        # 对于没有点击的用户，这种用户任务是无效用户，直接无视他的样本
        if len(row['click_id_list']) == 0:
            continue
        user_id = row['user_id']
        expose_id_list = list(set(row['expose_id_list']))
        click_id_list = list(set(row['click_id_list']))
        for item_id in expose_id_list:
            label = 1 if item_id in click_id_list else 0
            sample_list.append([user_id, item_id, label])
    sample_df = pd.DataFrame(sample_list, columns=['user_id', 'item_id', 'label'])
    return sample_df


def func_get_samples_feature_for_model(data_df, day, config):
        """
        将正负样本添加特征
        input
                                         user_id              item_id  label
            0   0959641A4DF1489580696B262CCDFA54  1875124086802522114      0
            1   0959641A4DF1489580696B262CCDFA54                50787      0

        """
        batch_size = 100
        batch_num = data_df.shape[0] // batch_size
        user_feature_all_dict = {}
        item_feature_all_dict = {}
        for i in range(batch_num+1):
            print('batch_num, batch_size, i: ', batch_num, batch_size, i)
            batch_df = data_df[i * batch_size : (i + 1) * batch_size]
            user_ids = list(set(batch_df['user_id'].tolist()))
            item_ids = list(set(batch_df['item_id'].tolist()))
            user_feature_dict = get_user_feature_batch_by_user_ids(user_ids, day, config)
            items_feature_dict = get_item_feature_batch_by_item_ids(item_ids, day, config)
            if len(user_feature_dict) > 0:
                user_feature_all_dict.update(user_feature_dict)
            if len(items_feature_dict) > 0:
                item_feature_all_dict.update(items_feature_dict)
        data_df['user_feature'] = data_df.apply(lambda row: user_feature_all_dict.get(row['user_id'], []) , axis=1)
        data_df['item_feature'] = data_df.apply(lambda row: item_feature_all_dict.get(row['item_id'], []) , axis=1)
        data_df['feature'] = data_df.apply(lambda row: row['user_feature'] + row['item_feature'] , axis=1)
        # 对于特征异常的过滤掉。主要是判断特征长度
        data_df = data_df[data_df['feature'].apply(lambda x: len(x) >= 6)]
        if 'label' in data_df.columns.values:
            data_df = data_df[['user_id', 'item_id', 'feature', 'label']]
            feature_df = pd.DataFrame(data_df['feature'].tolist(), index=data_df.index).astype('float32')
            label_df = data_df[['label']].astype('float32')
            return feature_df, label_df
        else:
            data_df = data_df[['user_id', 'item_id', 'feature']]
            feature_df = pd.DataFrame(data_df['feature'].tolist(), index=data_df.index).astype('float32')
            return feature_df



if __name__ == '__main__':
    """ 
    星河推荐 排序模型
    特征文档： http://cf.basestonedata.com:8090/pages/viewpage.action?pageId=488605081
    训练xgb模型 
    """
    config = get_env_config('uat')
    redis_dict = {'test': '1', 'uat': '1', 'prod': '1'}
    mysql_dict = {'test': '1', 'uat': '1', 'prod': '2'}
    redis_client = redis.StrictRedis(host=config['redis']['1']['host'],
                                     port=config['redis']['1']['port'],
                                     password=config['redis']['1']['password'])

    # 获取正负样本
    day_1 = time.strftime("%Y-%m-%d", time.localtime(time.time() - 1 * 60 * 60 * 24))
    day_2 = time.strftime("%Y-%m-%d", time.localtime(time.time() - 2 * 60 * 60 * 24))
    day_3 = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3 * 60 * 60 * 24))
    print(day_1, day_2, day_3)

    user_info = get_data_from_tablestore_sql_all_split_batch(f"""(
                        select *
                        from app_theatre_user_content_d_a_dt
                        where user_id REGEXP '[12345]$' and report_date='{day}'
                        )""", config, "1")
    print(user_info)
    sys.exit()

    samples_df = get_pn_samples(day_1)
    print(samples_df)
    print('正负样本的比例')
    print(samples_df[['label']].groupby('label').size())
    # 将正负样本添加特征
    feature_df, label_df = func_get_samples_feature_for_model(samples_df, day_2, config)
    print(feature_df)
    print(label_df)
    # 切分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(feature_df, label_df,test_size=0.2, random_state=42)
    dtrain = xgb.DMatrix(X_train, y_train)
    dtest = xgb.DMatrix(X_test, y_test)
    params = {
        'objective': "binary:logistic",
        "eta": 0.1,
        "max_depth": 6
    }
    num_rounds = 30
    bst = xgb.train(params, dtrain, num_rounds, evals=[(dtest, "test")])
    # 保存模型
    bst.save_model('model_file/xbg_model.model')
    test_pred = bst.predict(dtest)
    print(roc_auc_score(y_test, test_pred))
    y, pred = y_test, pd.DataFrame(test_pred)
    res = pd.concat([y.reset_index(drop=True), pred.reset_index(drop=True)], axis=1)
    print(res)
    print(res.sort_values(0, ascending=False).head(60))



"""

# redis_name = 'rank_item_feature'
# redis_client.expire(redis_name, 60*60*24)
# # redis_client.delete(redis_name)  # 存之前将旧redis清除
# for index, row in data_info.iterrows():
#     f_statistic = [row['expose_num_1'], row['click_num_1'], row['duration_1'], row['click_rate_1'], row['duration_rate_1']]
#     f_vec_str = ','.join([str(item) for item in f_statistic])
#     redis_client.hset(name=redis_name, key=str(row['item_id']), value=f_vec_str)
#
# print(redis_client.hgetall(name=redis_name))
# print([float(item) for item in redis_client.hget(redis_name, '100063').decode('utf-8').split(',')])



def func_embedding_drama_word(word_string):
    # 将文字向量化
    rep = requests.post(url='http://model-emb-pub.hobby666.com/context/encode',
                        headers={'Content-Type': 'application/json'},
                        json={
                            "model_name": "bge-large",
                            "context_list": [word_string]
                        }).json()
    res = rep['result'][0]
    return res

data_info['desc_llm_vec'] = data_info.apply(lambda row: func_embedding_drama_word(row['describe']), axis=1)
def func_feature_deal(row):
    # 获取物品特征
    f_statistic = [row['expose_num_1'], row['click_num_1'], row['duration_1'], row['click_rate_1'], row['duration_rate_1']]
    return f_statistic
data_info['feature_vec'] = data_info.apply(lambda x: func_feature_deal(x), axis=1)
print(data_info[['item_id', 'feature_vec']])

"""