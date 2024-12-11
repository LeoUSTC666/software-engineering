from datetime import datetime
import pymysql
from pymysql import Error
from flask import Flask, jsonify,session
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..conn import get_db_connection

teacher_bp = Blueprint('teacher', __name__)
import pymysql
import secrets
import os

@teacher_bp.route('/teacher_login',methods = ['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_id = request.form['teacher_id']
        password = request.form['password']
        user = validate_teacher_login(teacher_id, password)
        if user:
            return redirect(url_for('teacher.teacher_home', username=user[1], teacher_id=teacher_id))
        else:
            return render_template('teacher_login.html', error='Invalid userid or password')
    return render_template('teacher_login.html')

@teacher_bp.route('/teacher_home')
def teacher_home():
    username = request.args.get('username')
    teacher_id = request.args.get('teacher_id')
    curr_evalution = []
    teacher_evalution = []
    current_class = None
    if teacher_id:
        print(1)
        raw_teacher_evalution = search_teacher_evalution(teacher_id)
        print("raw_teacher_evalution:", raw_teacher_evalution)
        for eval in raw_teacher_evalution:
            if eval[0] == current_class:
                curr_evalution.append((eval[1], eval[2]))
                print("curr_evalution:", curr_evalution)
            else:
                if current_class is None: # 初始化第一个
                    current_class = eval[0]
                else:
                    teacher_evalution.append((current_class, curr_evalution))
                    current_class = eval[0]
                    curr_evalution = [] # 清空
                curr_evalution.append((eval[1], eval[2]))
        if current_class is not None:
            teacher_evalution.append((current_class, curr_evalution))
        print("teacher_evalution:", teacher_evalution)
    image_path = get_user_image(teacher_id)
    return render_template('teacher_home.html', teacher_id = teacher_id, username=username, teacher_evalution=teacher_evalution, image_path=image_path)

@teacher_bp.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['image']
        username = request.form['username']  
        teacher_id = request.form['teacher_id']  
        directory = os.path.join(os.getcwd(), 'static\\images')
    if not os.path.exists(directory):
        os.makedirs(directory)
    username = request.form['username']  
    teacher_id = request.form['teacher_id']  
    filename = os.path.join(directory, file.filename)
    file.save(filename)
    filename = '../static/images/' + file.filename
    save_to_db(teacher_id, filename)
    return redirect(url_for('teacher.teacher_home', teacher_id=teacher_id, username=username))


# def get_db_connection():
#     try:
#         conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='evalution_system', charset='utf8')
#         return conn
#     except pymysql.MySQLError as e:
#         print(f"Error connecting to the database: {e}")
#         return None

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
    
def save_to_db(teacher_id,filename):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        #查询数据库中是否有该用户的图片路径
        cursor.execute("SELECT * FROM images WHERE TEACHER_ID = %s", (teacher_id,))
        user = cursor.fetchone()
        #如果没有就插入
        if not user:
            query = "INSERT INTO images (teacher_id, image_path) VALUES (%s, %s)"
            params = (teacher_id, filename)
            cursor.execute(query, params)
            conn.commit()
            cursor.close()
            conn.close()
            return
        # 更新数据库中的文件路径
        query = "UPDATE images SET image_path = %s WHERE teacher_id = %s"
        params = (filename, teacher_id)
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(e)

def get_user_image(TEACHER_ID):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            #print(username)
            cursor.execute("SELECT image_path FROM images WHERE TEACHER_ID = %s", (TEACHER_ID,))
            image_path = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return image_path
        except Error as e:
            print(e)



def teacher_init_routes(app):
    app.register_blueprint(teacher_bp)