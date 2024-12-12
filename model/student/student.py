from datetime import datetime
import pymysql
from pymysql import Error
from flask import Flask, jsonify
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..conn import get_db_connection

student_bp = Blueprint('student', __name__)
import pymysql
import secrets

@student_bp.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form['student_id']
        password = request.form['password']
        # print("id: ", student_id)
        # print("password: ", password)
        user = validate_student_login(student_id, password)
        # print("user: ", user)
        if user:
            return redirect(url_for('student.student_home', username=user[3], stu_id=student_id))
        else:
            return render_template('student_login.html', error='Invalid username or password')
    return render_template('student_login.html')

@student_bp.route('/student_home')
def student_home():
    username = request.args.get('username')
    stu_id = request.args.get('stu_id')
    stu_evalution = None
    stu_class = None
    if stu_id:
        # print(1)
        stu_evalution = search_student_evalution(stu_id)
        # print("stu_evalution:", stu_evalution)
        stu_class = search_student_class(stu_id)
        # print("stu_class:", stu_class)
    return render_template('student_home.html', stu_id = stu_id, username=username, stu_evalution=stu_evalution, stu_class=stu_class)

@student_bp.route('/submit_emoji', methods=['POST'])
def submit_emoji():
    data = request.get_json()
    # print(99)
    student_id = data['student_id']
    class_id = data['class_id']
    emoji_code = data['emoji_code']
    print("student_id:", student_id)
    print("class_id:", class_id)
    print("emoji_code:", emoji_code)
    success = insert_student_evalution(student_id, class_id, emoji_code)
    if success:
        return jsonify({'message': '评价已提交'}), 200
    else:
        return jsonify({'message': '提交失败'}), 500
    
@student_bp.route('/delete_evalution', methods=['POST'])
def delete_evalution():
    data = request.get_json()
    evalution_id = data['evalution_id']
    success = delete_student_evalution(evalution_id)
    if success:
        return jsonify({'message': '评价已删除'}), 200
    else:
        return jsonify({'message': '删除失败'}), 500
    
@student_bp.route('/register', methods=['GET', 'POST'])
def register():
    print(10000)
    if request.method == 'POST':
        print(20000)
        student_name = request.form['student_name']
        student_id = request.form['student_id']
        nickname = request.form['nickname']
        password = request.form['verify_password']
        new_password = request.form['login_password']
        can_register, message = can_register_student(student_id, student_name, password)
        print(can_register)
        if can_register:
            success, message = register_student(student_id, student_name, nickname, new_password)
            if success:
                flash(message)
                return redirect(url_for('student.student_login'))
            else:
                flash(message)
        else:
            if message == "error_password":
                flash("校验密码错误！")
            elif message == "this student has already registered":
                flash("账号已经注册！")
            elif message == "invalid_student":
                flash("学生ID或姓名不匹配！")
            else:
                flash(message)
    return render_template('register.html')

# def get_db_connection():
#     try:
#         conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='evalution_system', charset='utf8')
#         return conn
#     except pymysql.MySQLError as e:
#         print(f"Error connecting to the database: {e}")
#         return None

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
        WHERE sc.STU_ID = %s
        """
        cursor.execute(sql, (student_id,))
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
        sql2 = "UPDATE TABLE_CHANGE_LOG SET IS_CHANGED = 1 WHERE CHANGE_ID = 1"
        cursor.execute(sql2)
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
        sql = "SELECT * FROM USER_STUDENT WHERE USER_STU_ID = %s AND STUDENT_PASSWORD = %s"
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

def can_register_student(student_id, student_name, password):
    conn = get_db_connection()
    if conn is None:
        return False, "数据库连接失败"
    try:
        cursor = conn.cursor()
        sql = "SELECT STU_PASSWORD, FLAG FROM STU_INFO WHERE STU_ID = %s AND STU_NAME = %s"
        cursor.execute(sql, (student_id, student_name))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            stu_password, flag = result
            if flag == 0:
                if password == stu_password:
                    return True, "ok"
                else:
                    return False, "error_password"
            else:
                return False, "this student has already registered"
        else:
            return False, "invalid_student"
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return False, "数据库查询失败"

def register_student(student_id, student_name, nickname, password):
    conn = get_db_connection()
    if conn is None:
        return False, "数据库连接失败"
    try:
        cursor = conn.cursor()
        # 插入新用户信息到USER_STUDENT表中
        sql_insert = "INSERT INTO USER_STUDENT (STUDENT_ID, STUDENT_NAME, STUDENT_NICKNAME, STUDENT_PASSWORD) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_insert, (student_id, student_name, nickname, password))
        # 更新STU_INFO表中的FLAG字段
        sql_update = "UPDATE STU_INFO SET FLAG = 1 WHERE STU_ID = %s"
        cursor.execute(sql_update, (student_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "注册成功"
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return False, "数据库操作失败"

def student_init_routes(app):
    app.register_blueprint(student_bp)