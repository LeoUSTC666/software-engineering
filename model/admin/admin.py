from datetime import datetime
import pymysql
from pymysql import Error
from flask import Flask, jsonify
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..conn import get_db_connection


admin_bp = Blueprint('admin', __name__)
import pymysql
import secrets



@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']
        user = validate_admin_login(admin_id, password)
        if user:
            print(1)
            return redirect(url_for('admin.admin_home'))
        else:
            return render_template('admin_login.html', error='Invalid admin_id or password')
    return render_template('admin_login.html')

@admin_bp.route('/admin_home')
def admin_home():
    raw_teacher_evalution = search_all_teacher_evalution()
    raw_student_evalution = search_all_student_evalution()
    # 处理数据，将其按教师分组
    charts_data = {}
    for eval in raw_teacher_evalution:
        teacher_name, class_name, emoji_code, emoji_count = eval
        if teacher_name not in charts_data:
            charts_data[teacher_name] = {}
        if class_name not in charts_data[teacher_name]:
            charts_data[teacher_name][class_name] = []
        charts_data[teacher_name][class_name].append({'emoji_code': emoji_code, 'count': emoji_count})

    return render_template('admin_home.html', charts_data=charts_data,student_evalution=raw_student_evalution)

@admin_bp.route('/delete_evalution', methods=['POST'])
def delete_evalution():
    data = request.get_json()
    evalution_id = data['evalution_id']
    success = delete_student_evalution(evalution_id)
    if success:
        return jsonify({'message': '评价已删除'}), 200
    else:
        return jsonify({'message': '删除失败'}), 500

# def get_db_connection():
#     try:
#         conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='evalution_system', charset='utf8')
#         return conn
#     except pymysql.MySQLError as e:
#         print(f"Error connecting to the database: {e}")
#         return None
    
def create_admin_account(admin_id, admin_name, admin_password):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO USER_ADMIN (ADMIN_ID, ADMIN_NAME, ADMIN_PASSWORD) VALUES (%s, %s, %s)"
        cursor.execute(sql, (admin_id, admin_name, admin_password))
        conn.commit()
        cursor.close()
        conn.close()
        return True
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
        sql2 = "UPDATE TABLE_CHANGE_LOG SET IS_CHANGED = 1 WHERE CHANGE_ID = 1"
        cursor.execute(sql2)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None

def search_all_student_evalution():
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = """
        SELECT e.EVALUTION_ID, s.STUDENT_NAME, c.CLASS_ID, c.CLASS_NAME, t.TEACHER_NAME, e.EMOJI_CODE, e.EVALUTION_DATE
        FROM EVALUTION e
        JOIN CLASS_INFO c ON e.CLASS_ID = c.CLASS_ID
        JOIN USER_STUDENT s ON e.STUDENT_ID = s.STUDENT_ID
        JOIN USER_TEACHER t ON c.CLASS_TEACHER_ID = t.TEACHER_ID
        ORDER BY s.STUDENT_NAME, c.CLASS_NAME
        """
        cursor.execute(sql)
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

def search_is_changed():
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = """
        call SELECT_TABLE_CHANGE_LOG()
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result[0][0]
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None
    
def admin_init_routes(app):
    app.register_blueprint(admin_bp)
    return app