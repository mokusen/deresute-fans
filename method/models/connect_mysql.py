import pymysql.cursors
import datetime
import method.models.handle_yaml as handle_yaml


def __connect():
    setting = handle_yaml.getSetting()
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
            (`idol_name`, `create_ts`, `update_ts`)
            values(%s, %s, %s)'''

            for idol_name in idol_name_list:
                cursor.execute(sql, (idol_name,
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


def select_idot_base():
    con = __connect()
    try:
        with con.cursor() as cursor:
            sql = 'select idol_name from delesute.idol_base'
            cursor.execute(sql)
            result = [idol_name_dict["idol_name"] for idol_name_dict in cursor.fetchall()]
    finally:
        con.close()
        return result
