# -*- coding: utf-8 -*-
"""
    :作者: Kavin
    :日期：2023/08/01
"""
from gevent import monkey
monkey.patch_all()

from flask import Flask, request, abort
import json
from service.ai_helper import AiHelper

import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

ai_helper = AiHelper()


# 获取订阅词
@app.route("/recommend/terms", methods=["GET"])
def get_subscription_terms():
    all_subscription_terms = json.load(open("./resource/subscription_terms.json", "r", encoding="utf-8"))
    user_id = request.args.to_dict()["user_id"]
    user_subscription_terms = ai_helper.get_user_subscribe_terms(user_id)
    result = {
        "code": 200,
        "message": "请求成功",
        "data": {
            "is_subscribe": 1 if user_subscription_terms else 0,
            "user_subscription_terms": user_subscription_terms,
            "all_subscription_terms": all_subscription_terms
            }
    }
    return json.dumps(result, ensure_ascii=False)

# 保存用户订阅信息
@app.route("/user/terms", methods=["POST"])
def save_user_term():
    if request.method == "POST":
        try:
            request_params = request.get_json()
            logger.info('user/terms request params:{}'.format(request_params))
            ai_helper.save_user_term(request_params)
            result = {
                "code": 200,
                "message": "请求成功"
            }
        except Exception as e:
            result = {
                "code": 0,
                "message": str(e)
            }
    logger.info('user/terms response data:{}'.format(result))
    return json.dumps(result, ensure_ascii=False)


# 保存资讯信息
@app.route("/article/sync", methods=["POST"])
def save_article_list():
    if request.method == "POST":
        try:
            request_params = request.get_json()
            logger.info('user/terms request params:{}'.format(request_params))
            ai_helper.save_article_list(request_params)
            result = {
                "code": 200,
                "message": "请求成功"
            }
        except Exception as e:
            result = {
                "code": 0,
                "message": str(e)
            }
    logger.info('user/terms response data:{}'.format(result))
    return json.dumps(result, ensure_ascii=False)

# 获取用户历史资讯列表
@app.route("/user/articles", methods=["GET"])
def get_user_article_history_list():
    try:
        user_id = request.args.to_dict()["user_id"]
        article_list = ai_helper.get_user_article_history_list(user_id)
        result = {
            "code": 200,
            "message": "请求成功",
            "data": article_list
        }
    except Exception as e:
        result = {
            "code": 0,
            "message": str(e)
        }
    logger.info('user/terms response data:{}'.format(result))
    return json.dumps(result, ensure_ascii=False)


# 定时推送用户资讯
@app.route("/recommend/articles", methods=["POST"])
def get_recommend_article_list():
    request_params = request.get_json()
    user_id = request_params.get("user_id")
    result = ai_helper.get_recommend_article_list(user_id)


# 用户关注/取消关注公众号接口
@app.route("/user/app_follow", methods=["POST"])
def update_app_follow():
    request_params = request.get_json()
    signature = request_params.get("signature")
    timestamp = request_params.get("timestamp")
    nonce = request_params.get("nonce")
    echostr = request_params.get("echostr")

    # 校验次数
    if not all([signature, timestamp, nonce, echostr]):
        abort(400)

    # 按照微信流程进行计算机签名

    ai_helper.update_app_follow(appid, openid, status)


if __name__ == '__main__':
    from gevent import pywsgi
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="the port for sevice",  type=int, default=8541)
    args = parser.parse_args()
    app.debug = True
    server = pywsgi.WSGIServer(('0.0.0.0', args.port), app)
    server.serve_forever()
    #app.run(debug = True,port=5000)

