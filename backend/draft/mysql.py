import pymysql
from dbutils.pooled_db import PooledDB
import pandas as pd


class MysqlOperation:
    def __init__(self, host="172.20.60.49", 
                       user="tensorfly", 
                       password="tensorfly", 
                       port=3306, 
                       database="ai_helper", 
                       connect_timeout=60, 
                       read_timeout=60, 
                       write_timeout=60):
        self.pool = PooledDB(host=host,
                             port=port,
                             user=user,
                             password=password,
                             database=database,
                             creator=pymysql,  # 使用链接数据库的模块
                             mincached=10,  # 初始化时，链接池中至少创建的链接，0表示不创建
                             maxconnections=200,  # 连接池允许的最大连接数，0和None表示不限制连接数
                             blocking=True)  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    def open(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 表示读取的数据为字典类型 cursor=pymysql.cursors.DictCursor
        return self.conn, self.cursor

    def close(self, cursor, conn):
        cursor.close()
        conn.close()

    def execute(self, sql, args, isNeed=False):
        """
        执行
        :param isNeed 是否需要回滚
        """
        conn, cursor = self.open()
        if isNeed:
            try:
                cursor.execute(sql, args)
                conn.commit()
            except:
                conn.rollback()
                raise
        else:
            cursor.execute(sql, args)
            conn.commit()
        self.close(conn, cursor)

    def get_user_terms(self, user_id):
        self.get_user_count(user_id)
        sql = "select term_id from user_term_mapping where user_id='" + user_id + "'"
        try:
            conn, cursor = self.open()    
            cursor.execute(sql)
            result = cursor.fetchall()
            self.close(conn, cursor)
            return [record["term_id"] for record in result]
        except Exception as e:
            raise


    """删除数据"""
    def delete_term_by_userid(self, user_id, *args):
        sql = "delete from user_term_mapping where user_id='" + user_id + "'"
        self.execute(sql, args, isNeed=True)

    def save_user_term(self, user_id, term_ids):
        """插入多条批量插入"""
        conn, cursor = self.open()
        records = [(user_id, term_id) for term_id in term_ids]
        sql = 'insert into user_term_mapping values (%s,%s)'
        try:
            cursor.executemany(sql, records)
            conn.commit()
        except Exception as err:
            conn.rollback()
            raise
        self.close(conn, cursor)

    def get_user_count(self, user_id):
        conn, cursor = self.open()
        sql = "select count(user_id) as total from user_term_mapping where user_id='" + user_id + "'"
        cursor.execute(sql)
        result = cursor.fetchone()["total"]
        self.close(conn, cursor)
        return result


    def get_article_ids(self, user_id):
        sql = "select article_id from user_article_mapping where user_id='" + user_id + "'"
        try:
            conn, cursor = self.open()
            cursor.execute(sql)
            result = cursor.fetchall()
            self.close(conn, cursor)
            return [record["article_id"] for record in result]
        except Exception as e:
            raise

    def update_app_follow(self, appid_, open_id_, user_id_, status_):
        conn, cursor = self.open()
        # 删除旧数据
        sql = "delete from app_follow where appid='%s' and user_id='%s'" % (appid_, user_id_)
        cursor.execute(sql)
        conn.commit()
        # 插入新数据
        sql = "INSERT INTO app_follow(appid, user_id, openid, status) VALUES('%s','%s','%s','%s')" % (appid_, user_id_, open_id_, status_)
        cursor.execute(sql)
        conn.commit()

    def get_app_follow_id(self):
        conn, cursor = self.open()
        sql = "select user_id from app_follow "
        cursor.execute(sql)
        result = cursor.fetchall()
        return [record["user_id"] for record in result]

    def get_app_follow_data(self):
        conn, cursor = self.open()
        sql = "select *  from app_follow"
        cursor.execute(sql)
        conn.commit()
