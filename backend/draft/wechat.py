import time

import requests
import json

import service.ai_helper
from service.mysql import MysqlOperation

from service import ai_helper


def get_access_token(appID, app_secret):
    """
    获取access_token，通过查阅微信公众号的开发说明就清晰明了了
    读取数据文件，如果  当前时间-写入时间 < 1h, 直接使用，否则重新获取token
    """

    def product_access_token():
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appID, app_secret)
        response = requests.get(url).json()
        access_token = response.get('access_token')
        print("product_access_token", access_token)
        # access_token = "uhiluhliughoiugiuglugliu" + str(int(time.time()))
        return access_token

    with open("access_token.txt", 'r') as f:
        lines = f.readlines()
        print("======", lines, len(lines))

    with open("access_token.txt", 'w+') as f:
        if len(lines) == 0:
            token = product_access_token()
            product_token_time = time.time()
            content = (token + "," + str(product_token_time)).strip()
            f.write(content)
            print("null and product token")
            return token
        for line in lines:
            row = line.strip().split(",")
            token = row[0]
            product_token_time = row[1]
            use_token_time = time.time()
            if use_token_time - float(product_token_time) < 3600:
                content = (token + "," + str(product_token_time)).strip()
                f.write(content)
                print("get_from_file")
                return token
            else:
                token = product_access_token()
                product_token_time = time.time()
                content = (token + "," + str(product_token_time)).strip()
                f.write(content)
                print("timeout product token")
                return token


# def get_user_info():
#     """
#     获取用户信息
#     """
#     # 获取所有用户的openid，微信公众号开发文档中可以查阅获取openid的方法
#     appid = "wx3cb3ce23650293c9"
#     app_secret = "c8de8702fa1053f347a2524793d042b3"
#     access_token = get_access_token(appid, app_secret)
#     next_openid = ''
#     url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (
#     access_token, next_openid)
#     ans = requests.get(url_openid)
#     open_ids = json.loads(ans.content)['data']['openid']
#     # 获取用户信息
#     for open_id in open_ids:
#         url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (
#         access_token, open_id)
#         ans = requests.get(url)
#         unionid = json.loads(ans.content)['unionid']
#         print(appid, open_id, unionid)


if __name__ == "__main__":
    # t = service.ai_helper.AiHelper()
    # t.update_app_follow(appid="wx3cb3ce23650293c9", status=1)
    # mysql_op = MysqlOperation()
    # mysql_op.get_app_follow_data()
    appid = "wx3cb3ce23650293c9"
    app_secret = "c8de8702fa1053f347a2524793d042b3"
    access_token = get_access_token(appid, app_secret)
    print(access_token)



