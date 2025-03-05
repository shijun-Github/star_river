import json
import sys
import time
from pprint import pprint


sys.path.append('../..')  # 假设'..'是drama和utils的父目录
from aa_recommend_complete_project.recall import base_rec

# from aa_recommend_complete_project.recall.hot import hot_recall_click_rate
# from utils.config_constants import get_env_config
# from utils.func_mysql import get_data_from_mysql


# def comb_all_recall(parm):
#     """ 获取各路召回， 然后排序"""
#     t = hot_recall_click_rate(parm)
#     return t


def func_main_run(parm):
    func_random_get_video = base_rec.func_random_get_video(parm)
    res_df = func_random_get_video
    res_list_dict = res_df.to_dict(orient='records')

    pprint(res_list_dict[0])
    print(res_list_dict[0]['video_url'])
    return res_list_dict

    #
    # df_ = comb_all_recall(parm)
    # print(df_)
    # # print(df_[['source', 'theatre_id', 'extend', 'describe']])
    #
    # df_deal = df_
    # # df_deal = df_deal.sort_values(by=['click_rate'])
    # # df_deal = shuffle(df_deal)
    # res = []
    # if df_deal.shape[0] > 0:
    #     df_deal = df_deal[(parm['page_index'] - 1) * parm['page_size']: parm['page_index'] * parm['page_size']]
    #     # df_deal = df_deal.sort_values('publish_time', ascending=False)
    #     for index, row in df_deal.iterrows():
    #         res.append({
    #             'item_id': row['item_id'],
    #             'item_name': row['video_title'],
    #             'author_name': json.loads(row['extend'])['name'],
    #             'cover_url': row['cover_url'],
    #             'video_url': row['video_url']
    #             # 'extend': {
    #             #     # 'cover_url': row['cover_url'],
    #             #     # 'video_url': row['video_url'],
    #             #     # 'video_duration': row['video_duration']
    #             # }
    #         })
    # pprint(res)
    # res = res[:3] + res
    # return res


if __name__ == '__main__':
    """ 主推荐页 """
    req = {
        'user_id': '11111',
        'page_index': 1,
        'page_size': 10,
    }
    t = func_main_run(req)
    pprint(t)


