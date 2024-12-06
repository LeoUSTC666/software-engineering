'''
Descripttion: 
version: 
Author: Leo
Date: 2024-11-30 19:15:18
LastEditors: Leo
LastEditTime: 2024-12-06 21:59:42
'''
from datetime import datetime
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
        sql = """
        SELECT e.EVALUTION_ID, e.STUDENT_ID, c.CLASS_NAME, t.TEACHER_NAME, e.EMOJI_CODE, e.EVALUTION_DATE
        FROM EVALUTION e
        JOIN CLASS_INFO c ON e.CLASS_ID = c.CLASS_ID
        JOIN USER_TEACHER t ON c.CLASS_TEACHER_ID = t.TEACHER_ID
        WHERE e.STUDENT_ID = %s
        """
        cursor.execute(sql, (student_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None

def search_teacher_evalution(teacher_id):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = """
        SELECT c.CLASS_NAME, e.EMOJI_CODE, COUNT(e.EMOJI_CODE) as emoji_count
        FROM EVALUTION e
        JOIN CLASS_INFO c ON e.CLASS_ID = c.CLASS_ID
        JOIN USER_TEACHER t ON c.CLASS_TEACHER_ID = t.TEACHER_ID
        WHERE t.TEACHER_ID = %s
        GROUP BY c.CLASS_NAME, e.EMOJI_CODE
        ORDER BY c.CLASS_NAME
        """
        cursor.execute(sql, (teacher_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None
    
def search_all_teacher_evalution():
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = """
        SELECT t.TEACHER_NAME, c.CLASS_NAME, e.EMOJI_CODE, COUNT(e.EMOJI_CODE) as emoji_count
        FROM EVALUTION e
        JOIN CLASS_INFO c ON e.CLASS_ID = c.CLASS_ID
        JOIN USER_TEACHER t ON c.CLASS_TEACHER_ID = t.TEACHER_ID
        GROUP BY t.TEACHER_NAME, c.CLASS_NAME, e.EMOJI_CODE
        ORDER BY t.TEACHER_NAME, c.CLASS_NAME
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None

def search_student_class(student_id):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = """
        SELECT c.CLASS_ID, c.CLASS_NAME, t.TEACHER_NAME
        FROM CLASS_INFO c
        JOIN USER_TEACHER t ON c.CLASS_TEACHER_ID = t.TEACHER_ID
        JOIN CLASS_STUDENT sc ON c.CLASS_ID = sc.CLASS_ID
        WHERE sc.STUDENT_ID = %s
        """
        cursor.execute(sql, (student_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None
    
def search_teacher_class(teacher_id):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = """
        SELECT c.CLASS_ID, c.CLASS_NAME, t.TEACHER_NAME
        FROM CLASS_INFO c
        JOIN USER_TEACHER t ON c.CLASS_TEACHER_ID = t.TEACHER_ID
        WHERE t.TEACHER_ID = %s
        """
        cursor.execute(sql, (teacher_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None

def insert_student_evalution(student_id, class_id, emoji_code):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO evalution (student_id, class_id, emoji_code, evalution_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (student_id, class_id, emoji_code,datetime.now()))
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
    
def  validate_teacher_login(teacher_id, password):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM USER_TEACHER WHERE TEACHER_ID = %s AND TEACHER_PASSWORD = %s"
        cursor.execute(sql, (teacher_id, password))
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
    
def validate_admin_login(admin_id, password):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM USER_ADMIN WHERE ADMIN_ID = %s AND ADMIN_PASSWORD = %s"
        cursor.execute(sql, (admin_id, password))
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

def delete_student_evalution(evalution_id):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM evalution WHERE evalution_id = %s"
        cursor.execute(sql, (evalution_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None
    