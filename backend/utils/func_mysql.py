import pymysql
import pandas as pd


def func_get_data_from_mysql(sql_input):
    """ 从mysql中获取数据， mysql_config 为使用配置文件中那个mysql """
    with pymysql.connect(host='localhost', port=3306, user='root', password='2019_shjw') as conn:
        cursor = conn.cursor()
        cursor.execute(sql_input)
        des = cursor.description  # 拿到表头
        title = [each[0] for each in des]
        results = cursor.fetchall()  # 获取所有记录列表
        data_df = pd.DataFrame(results, columns=title)  # 保存成dataframe
        return data_df


def func_save_data_to_mysql(sql_input):
    """ 将数据存储到mysql表中 """
    pass


def func_create_mysql_table(sql_input):
    """ 创建mysql表
    DROP TABLE IF EXISTS goods.jd_goods_info_ori;

    CREATE TABLE IF NOT EXISTS goods.jd_goods_info_ori (
       item_id VARCHAR(50) NOT NULL DEFAULT '0',
       info JSON,
       status VARCHAR(50) NOT NULL DEFAULT '0',
       PRIMARY KEY (item_id)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8
    """
    with pymysql.connect(host='localhost', port=3306, user='root', password='2019_shjw') as conn:
        cursor = conn.cursor()
        cursor.execute(sql_input)
        conn.commit()


def func_delete_mysql_table(sql_input):
    """ 创建mysql表 """
    """ 创建mysql表
    DROP TABLE IF EXISTS goods.jd_goods_info_ori
    """
    with pymysql.connect(host='localhost', port=3306, user='root', password='2019_shjw') as conn:
        cursor = conn.cursor()
        cursor.execute(sql_input)
        conn.commit()


def func_delete_data_in_mysql_table(sql_input):
    """ 创建mysql表 """
    pass


def func_insert_data_into_mysql_table(sql_input):
    """
    将数据插入表格中
        1、https://cloud.tencent.com/developer/article/1375845
        2、replace into相当于，先检测该记录是否存在(根据表上的唯一键)，如果存在，先delete，然后再insert。
        这个方法有一个很大的问题，如果记录存在，每次执行完，主键自增id就变了（相当于重新insert了一条），
        对于有复杂关联的业务场景，如果主表的id变了，其它子表没做好同步，会死得很难看。-- 不建议使用该方法！
    """
    with pymysql.connect(host='localhost', port=3306, user='root', password='2019_shjw') as conn:
        cursor = conn.cursor()
        cursor.execute(sql_input)
        conn.commit()


