'''
Descripttion: 
version: 
Author: Leo
Date: 2024-11-29 17:00:10
LastEditors: Leo
LastEditTime: 2024-11-30 18:15:54
'''
from datetime import datetime
from flask import Flask, request, render_template, url_for, redirect

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
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM USER_STUDENT WHERE STUDENT_ID = %s AND STUDENT_PASSWORD = %s', (student_id, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            user = User(user[0], user[1], user[2])
            return redirect(url_for('student_home', username=user.username))
        else:
            return render_template('student_login.html', error='Invalid username or password')
    return render_template('student_login.html')

@app.route('/student_home')
def student_home():
    username = request.args.get('username')
    return f"Welcome, {username}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)