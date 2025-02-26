# -*- coding: utf-8 -*-
import pandas as pd
import requests
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler

from backend.goods.data_get_jd_goods_info import func_get_goods_info_jd
from backend.goods.rank_goods_home_recommend import func_main_goods_home_recommend
# from backend.video.rank_drama_home_recommend import func_main_video_home_recommend
from backend.video import rank_drama_home_recommend
pd.set_option('expand_frame_repr', False)  # 显示的时候不换行
pd.set_option('display.max_columns', None)  # 显示所有列


app = Flask(__name__)


@app.route("/user/get_wx_login_code", methods=["POST"])
def get_wx_login_code():
    # 获取用户登录code
    # print(request)
    req = request.get_json()
    req['AppID'] = 'wx316d550728fad5d7'
    req['AppSecret'] = '9226316899b2f5459c94c8e7b5a3e8b4'
    print('get_wx_login_code============ ', req)
    url_ = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + \
           req['AppID'] + '&secret=' + req['AppSecret'] + '&js_code=' + \
           req['code'] + '&grant_type=authorization_code'
    res = requests.post(json=req,
                        url=url_,
                        headers={'content-type': 'application/json'},
                        timeout=30).json()
    print('-后端返回的结果 用户', res)
    return res

@app.route('/goods/home/recommend', methods=['POST'])
def predict_generate_image():
    """
curl.exe -X POST 'http://127.0.0.1:8528/goods/home/recommend' -H 'Content-Type:application/json' -d '{"user_id":"oNfQV6XQaAornDjN6xg-9GOqnba8", "page_index": 1, "page_size": 10}'
    """
    try:
        input_parameter = request.get_json()
        print(input_parameter)
        parm = {
            'page_index': input_parameter['page_index'],
            'page_size': input_parameter['page_size'],
            'channel': int(input_parameter['channel'])
        }
        res_return = func_main_goods_home_recommend(parm)
        res = {'res_data': res_return, 'num': len(res_return)}
        print(res)
    except Exception as ex:
        res = ex
    return res


@app.route('/video/home/recommend', methods=['POST'])
def predict_video_home_recommend():
    """
curl.exe -X POST 'http://127.0.0.1:8528/goods/home/recommend' -H 'Content-Type:application/json' -d '{"user_id":"oNfQV6XQaAornDjN6xg-9GOqnba8", "page_index": 1, "page_size": 10}'
    """
    try:
        input_parameter = request.get_json()
        print(input_parameter)
        parm = {
            'page_index': input_parameter['page_index'],
            'page_size': input_parameter['page_size'],
            'channel': input_parameter['channel']
        }
        res_return = rank_drama_home_recommend.func_main_goods_home_recommend(parm)
        res = {'res_data': res_return, 'num': len(res_return)}
        print(type(res['res_data']), res)
    except Exception as ex:
        res = ex
    return res


def start_scheduler():
    """
    定时刷新数据
    :return:
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(func_get_goods_info_jd, 'interval', seconds=60*60*12)
    scheduler.start()


if __name__ == '__main__':
    """
    综合服务
    """
    # func_get_goods_info_jd()

    app.run(host='0.0.0.0', port=3337, debug=False)



