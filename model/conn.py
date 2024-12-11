import pymysql
from pymysql import Error

def get_db_connection():
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='leo520', db='evalution_system', charset='utf8')
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None