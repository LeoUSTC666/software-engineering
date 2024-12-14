
from time import sleep
from datetime import datetime
from flask_socketio import SocketIO, emit
from flask import Flask, request, render_template, url_for, redirect, jsonify
from flask_login import UserMixin  # 引入用户基类
from werkzeug.security import check_password_hash
from model.admin.admin import  create_admin_account, validate_admin_login, search_is_changed,admin_init_routes
from model.teacher.teacher import  validate_teacher_login, search_teacher_evalution,teacher_init_routes,save_to_db
from model.student.student import  validate_student_login, search_student_evalution, search_student_class, insert_student_evalution, delete_student_evalution,student_init_routes
from model.conn import get_db_connection
import pymysql
import os

pymysql.install_as_MySQLdb()

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = 'abc'  # 设置一个密钥用于会话管理
admin_init_routes(app)
teacher_init_routes(app)
student_init_routes(app)

app.config['SECRET_KEY'] = os.urandom(24)

# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='leo520', db='lab2', charset='utf8')

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @property
    def is_active(self):
        # 这里可以添加你的逻辑来判断用户是否活跃
        return True

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('refresh_request')
def refresh():
    #检测数据库是否有更新
    result = search_is_changed()
    print('result:', result)
    if result == 1:
        print('refresh!!!!!')
        emit('refresh_response', broadcast=True) 
    else:
        emit('no_refresh', broadcast=True)  

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(app,host='0.0.0.0', port=5000, debug=True)