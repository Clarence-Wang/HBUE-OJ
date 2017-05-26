# coding:utf-8
import types

import MySQLdb
import logging

import time

from judge import config


def run_sql(sql):
    while True:
        try:
            con = MySQLdb.connect(config.db_host, config.db_user, config.db_password,
                                  config.db_name, charset=config.db_charset)
            break
        except:
            logging.error("Cannot connect to database, try again")
            time.sleep(1)
    cur = con.cursor()
    try:
        if type(sql) == types.StringType:
            cur.execute(sql)
        elif type(sql) == types.ListType:
            for i in sql:
                cur.execute(i)
    except MySQLdb.OperationalError as e:
        logging.error(e)
        cur.close()
        con.close()
        return False
    con.commit()
    data = cur.fetchall()
    cur.close()
    con.close()
    return data
