'''
Descripttion: 
version: 
Author: Leo
Date: 2024-11-29 17:00:10
LastEditors: Leo
LastEditTime: 2024-12-02 14:56:03
'''
from datetime import datetime
from flask import Flask, request, render_template, url_for, redirect, jsonify
from sql_src.func import search_student_evalution, validate_student_login, search_student_class, insert_student_evalution

import pymysql
import os

pymysql.install_as_MySQLdb()

app = Flask(__name__)

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='leo520', db='lab2', charset='utf8')

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template('student_home.html', username=username, stu_evalution=stu_evalution, stu_class=stu_class)

@app.route('/submit_emoji', methods=['POST'])
def submit_emoji():
    data = request.get_json()
    print(99)
    student_id = data['student_id']
    class_id = data['class_id']
    emoji_code = data['emoji_code']
    success = insert_student_evalution(student_id, class_id, emoji_code)
    if success:
        return jsonify({'message': '评价已提交'}), 200
    else:
        return jsonify({'message': '提交失败'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)