'''
Descripttion: 
version: 
Author: Leo
Date: 2024-11-29 17:00:10
LastEditors: Leo
LastEditTime: 2024-12-01 18:04:22
'''
from datetime import datetime
from flask import Flask, request, render_template, url_for, redirect
from sql_src.func import search_student_evalution, validate_student_login

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
    if stu_id:
        print(1)
        stu_evalution = search_student_evalution(stu_id)
        print(stu_evalution)
    return render_template('student_home.html', username=username, stu_evalution=stu_evalution)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)