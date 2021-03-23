import pymysql
from pymysql.constants import CLIENT

con = pymysql.connect(host='',
                      port=,
                      user='',
                      password='',
                      database='',
                      autocommit=True,
                      client_flag=CLIENT.MULTI_STATEMENTS)
