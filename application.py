'''
Descripttion: 
version: 
Author: Leo
Date: 2024-11-29 17:00:10
LastEditors: Leo
LastEditTime: 2024-12-07 16:22:41
'''
from datetime import datetime
# from flask_socketio import SocketIO, emit
from flask import Flask, request, render_template, url_for, redirect, jsonify
from sql_src.func import get_user_image,save_to_db,search_student_evalution, validate_student_login, search_student_class, insert_student_evalution,delete_student_evalution, validate_teacher_login,search_teacher_evalution,search_all_teacher_evalution,validate_admin_login, search_all_student_evalution

import pymysql
import os

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='leo520', db='lab2', charset='utf8')

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']
        user = validate_admin_login(admin_id, password)
        if user:
            print(1)
            return redirect(url_for('admin_home'))
        else:
            return render_template('admin_login.html', error='Invalid admin_id or password')
    return render_template('admin_login.html')

@app.route('/admin_home')
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


@app.route('/teacher_login',methods = ['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        teacher_id = request.form['teacher_id']
        password = request.form['password']
        user = validate_teacher_login(teacher_id, password)
        if user:
            return redirect(url_for('teacher_home', username=user[1], teacher_id=teacher_id))
        else:
            return render_template('teacher_login.html', error='Invalid userid or password')
    return render_template('teacher_login.html')

@app.route('/teacher_home')
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

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form['student_id']
        password = request.form['password']
        user = validate_student_login(student_id, password)
        if user:
            return redirect(url_for('student_home', username=user[1], stu_id=student_id))
        else:
            return render_template('student_login.html', error='Invalid username or password')
    return render_template('student_login.html')

@app.route('/student_home')
def student_home():
    username = request.args.get('username')
    stu_id = request.args.get('stu_id')
    stu_evalution = None
    stu_class = None
    if stu_id:
        print(1)
        stu_evalution = search_student_evalution(stu_id)
        print("stu_evalution:", stu_evalution)
        stu_class = search_student_class(stu_id)
        print("stu_class:", stu_class)
    return render_template('student_home.html', stu_id = stu_id, username=username, stu_evalution=stu_evalution, stu_class=stu_class)

@app.route('/submit_emoji', methods=['POST'])
def submit_emoji():
    data = request.get_json()
    print(99)
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
    
@app.route('/delete_evalution', methods=['POST'])
def delete_evalution():
    data = request.get_json()
    evalution_id = data['evalution_id']
    success = delete_student_evalution(evalution_id)
    if success:
        return jsonify({'message': '评价已删除'}), 200
    else:
        return jsonify({'message': '删除失败'}), 500
    
@app.route('/upload/', methods=['GET', 'POST'])
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
    return redirect(url_for('teacher_home', teacher_id=teacher_id, username=username))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)