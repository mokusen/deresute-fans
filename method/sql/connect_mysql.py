from pathlib import Path
import pymysql.cursors
import datetime
from method.utils import handle_yaml


def __connect():
    setting_path = Path(__file__).parents[2].joinpath('setting.yml')
    setting = handle_yaml.get_yaml(setting_path)["mysql"]
    con = pymysql.connect(host=setting["host"],
                          user=setting["user"],
                          password=setting["pass"],
                          db=setting["db"],
                          cursorclass=pymysql.cursors.DictCursor)
    return con


def insert_idol_base(idol_name_list):
    con = __connect()
    try:
        with con.cursor() as cursor:
            sql = '''insert into `idol_base`
            (`idol_name`, `idol_alpha`, `create_ts`, `update_ts`)
            values(%s, %s, %s, %s)'''

            cursor.execute(sql, (idol_name_list[0],
                                 idol_name_list[1],
                                 datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        con.commit()
    finally:
        con.close()


def insert_idol_fans(id, fans, create_ts):
    con = __connect()
    try:
        with con.cursor() as cursor:
            sql = '''insert into `idol_fans`
            (`idol_id`, `fans`, `create_ts`)
            values(%s, %s, %s)'''

            cursor.execute(sql, (id,
                                 fans,
                                 create_ts))
        con.commit()
    finally:
        con.close()


def select_idol_base():
    con = __connect()
    try:
        with con.cursor() as cursor:
            sql = 'select idol_alpha from delesute.idol_base'
            cursor.execute(sql)
            result = [idol_name_dict["idol_alpha"] for idol_name_dict in cursor.fetchall()]
    finally:
        con.close()
        return result
