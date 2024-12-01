'''
Descripttion: 
version: 
Author: Leo
Date: 2024-11-30 19:15:18
LastEditors: Leo
LastEditTime: 2024-12-01 18:03:14
'''
import pymysql

def get_db_connection():
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='leo520', db='lab2', charset='utf8')
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None

def search_student_evalution(student_id):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM evalution WHERE student_id = %s"
        cursor.execute(sql, (student_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None

def delete_student_evalution(student_id, class_id, emoji_id):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM evalution WHERE student_id = %s and class_id = %s and emoji_id = %s"
        cursor.execute(sql, (student_id, class_id, emoji_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None

def validate_student_login(student_id, password):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM USER_STUDENT WHERE STUDENT_ID = %s AND STUDENT_PASSWORD = %s"
        cursor.execute(sql, (student_id, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return user
        else:
            return None
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None