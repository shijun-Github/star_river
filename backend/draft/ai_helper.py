import requests

from service.mysql import MysqlOperation
import service.elasticsearch as es_op
import time
import json


def get_access_token(appID, app_secret):
    """
    获取access_token，通过查阅微信公众号的开发说明就清晰明了了
    读取数据文件，如果  当前时间-写入时间 < 1h, 直接使用，否则重新获取token
    """
    def product_access_token():
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"% (appID, app_secret)
        response = requests.get(url).json()
        access_token = response.get('access_token')
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


class AiHelper:
    def __init__(self):
        self.mysql_op = MysqlOperation()

    def get_article_list(self, user_id):
        pass

    # 保存用户订阅信息
    def save_user_term(self, request_params):
        user_id = request_params["user_id"]
        term_ids = request_params["ids"]
        # 删除历史订阅信息
        self.mysql_op.delete_term_by_userid(user_id)
        # 插入新的订阅信息
        self.mysql_op.save_user_term(user_id, term_ids)

    # 保存爬虫爬取的消息
    def save_article_list(self, request_params):
        articles = request_params["articles"]
        es_op.save_article_list(articles)

    # 判断用户是否订阅
    def confirm_user_subscribe(self, user_id):
        record_count = self.mysql_op.get_user_count(user_id)
        return 1 if record_count else 0

    # 获取用户订阅词
    def get_user_subscribe_terms(self, user_id):
        return self.mysql_op.get_user_terms(user_id)


    #获取历史推送资讯
    def get_user_article_history_list(self, user_id):
        article_ids = self.mysql_op.get_article_ids(user_id)
        if article_ids:
            article_list = es_op.get_article_list(article_ids)
        else:
            article_list = []

        return article_list

    ## 将文章信息从es中同步一份到mysql中

    ## 获取用户关注文章推荐
    # 获取关注的用户ID，获取用户关注的关键词，获取文章关键词，==> 用户对应的文章
    def get_user_recommend_article(self):
        sql = '''
        SELECT af.user_id, ai.article_id, ai.pubblish_time
        FROM
            app_follow AS af
            LEFT JOIN user_term_mapping utp ON af.user_id = utp.user_id
            LEFT JOIN article_info ai ON utp.term_id = ai.term_id
        WHERE
            publish_time > ( unix_timestamp( now())- 1 * 86400 )* 1000
        '''


    # 用户关注/取消关注公众号接口
    def update_app_follow(self, appid, status):
        # 获取所有用户的openid，微信公众号开发文档中可以查阅获取openid的方法
        appid = "wx3cb3ce23650293c9"
        app_secret = "c8de8702fa1053f347a2524793d042b3"
        access_token = get_access_token(appid, app_secret)
        next_openid = ''
        url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (access_token, next_openid)
        ans = requests.get(url_openid)
        open_ids = json.loads(ans.content)['data']['openid']
        # 获取用户信息
        for open_id in open_ids:
            url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (access_token, open_id)
            ans = requests.get(url)
            unionid = json.loads(ans.content)['unionid']
            print(appid, open_id, unionid)
            self.mysql_op.update_app_follow(appid_=appid, open_id_=open_id, user_id_=unionid, status_=status)





