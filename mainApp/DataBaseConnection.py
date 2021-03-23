import pymysql
from pymysql.constants import CLIENT

con = pymysql.connect(host='127.0.0.1',
                      port=3306,
                      user='root',
                      password='root',
                      database='ciris_lib',
                      autocommit=True,
                      client_flag=CLIENT.MULTI_STATEMENTS)
