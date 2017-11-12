# -*- coding:utf-8 -*-

import login
import os
import sqlite3

from flask import Flask, redirect, request, url_for,render_template
from jinja2 import Environment, PackageLoader


from collections import namedtuple

app = Flask(__name__)
get = Environment(loader=PackageLoader(__name__, 'templates')).get_template


# 连接数据库sqlite3  数据库名: login.db
def open_database(path='login.db'):
    new = not os.path.exists(path)
    db = sqlite3.connect(path)
    
    return db 


#添加学生信息函数
def add_studentMessage(db, sno, sname, admin):
    cursor = db.cursor()
    cursor.execute('INSERT INTO student(SNO, SNAME, ADMIN) VALUES (?, ?, ?)', 
        (sno, sname, admin))

#显示学生信息函数
def get_studentMessage_of(db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM student;')
    Row = namedtuple('Row', [tup[0] for tup in cursor.description])
    return [Row(*row) for row in cursor.fetchall()]

#删除学生信息函数
def delete_studentMessage(db, sno):
    cursor = db.cursor()
    cursor.execute('DELETE FROM student WHERE sno=(?)', (sno))

#添加教师信息函数
def add_teacherMessage(db, tno, tname, sex, title):
    cursor = db.cursor()
    cursor.execute('INSERT INTO teacher(tno, tname, sex, title) VALUES (?, ?, ?, ?)', 
        (tno, tname, sex, title))

#显示教师信息函数
def get_teacherMessage_of(db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM teacher;')
    Row = namedtuple('Row', [tup[0] for tup in cursor.description])
    return [Row(*row) for row in cursor.fetchall()]

#删除教师信息函数
def delete_teacherMessage(db, tno, tname):
    cursor = db.cursor()
    cursor.execute('DELETE FROM teacher WHERE tno=? AND tname=?', 
        (tno, tname))

#添加课程信息函数
def add_courseMessage(db, cno, cname, tno, title):
    cursor = db.cursor()
    cursor.execute('INSERT INTO course(cno, cname, tno, title) VALUES (?, ?, ?, ?)', 
        (cno, cname, tno, title))

#显示课程信息函数
def get_courseMessage_of(db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM course')
    Row = namedtuple('Row', [tup[0] for tup in cursor.description])
    return [Row(*row) for row in cursor.fetchall()]

#删除课程信息函数
def delete_courseMessage(db, cno):
    cursor = db.cursor()
    cursor.execute('DELETE FROM course WHERE cno=?', cno)


#显示登陆界面
@app.route('/', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (username, password) in [('jia', '2015'), ('jack', '2015')]:
            response = redirect(url_for('index'))
            response.set_cookie('username', username)
            return response
    return get('login.html').render(username=username)




#显示首页
@app.route('/index')
def index():
    return render_template('index.html')


#退出
@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.set_cookie('username', '')
    return response    

#显示404页面
@app.route('/page404')
def __404__():
    return render_template('404.html')

#显示学生信息
@app.route('/studentMessage')
def studentMessage():    
    db = open_database()

    Message = get_studentMessage_of(db)
    
    return render_template('studentMessage.html', Message = Message)


#添加学生信息
@app.route('/student', methods=['GET', 'POST'])
def student():             
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('/'))
    student_id = request.form.get('student_id', '').strip()
    student_name  = request.form.get('student_name', '').strip()
    complaint = None
    if request.method == 'POST':
        if student_id and student_name and student_id.isdigit():
            db = open_database()
            add_studentMessage(db,student_id, student_name, username)
            db.commit()
            return redirect(url_for('studentMessage', flash='send successful'))
        complaint = ('username must be text' if not student_id.isdigit()
                     else 'Please fill in all three fields')
    return get('student.html').render(complaint=complaint, student_id=student_id,
                                      student_name=student_name)

#删除学生信息
@app.route('/delete_studentMessage', methods=['GET', 'POST'])
def delete_studentMessage():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('/'))

    student_id = request.form.get('student_id', '').strip()
    complaint = None
    if request.method == 'POST':
        if student_id and student_id.isdigit():
            db = open_database()
            delete_studentMessage(db, student_id)
            db.commit()
            return redirect(url_for('delete_studentMessage', flash='send successful'))
        complaint = ('username must be text' if not student_id.isdigit()
                     else 'Please fill in all three fields')
    return get('delete_studentMessage.html').render(complaint=complaint, student_id=student_id)


#添加教师信息
@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    teacher_id = request.form.get('teacher_id', '').strip()
    teacher_name = request.form.get('teacher_name', '').strip()
    teacher_sex = request.form.get('teacher_sex', '').strip()
    teacher_title = request.form.get('teacher_title', '').strip()
    complaint = None
    if request.method == 'POST':
        if teacher_id and teacher_name and teacher_id.isdigit():
            db = open_database()
            add_teacherMessage(db, teacher_id, teacher_name, teacher_sex, teacher_title)
            db.commit()
            return redirect(url_for('teacher', flash='send successful'))
        complaint = ('username must be text' if not teacher_id.isdigit()
                     else 'Please fill in all three fields')
    return get('teacher.html').render(complaint=complaint, teacher_id=teacher_id,
        teacher_name=teacher_name, teacher_sex=teacher_sex, teacher_title=teacher_title)

#显示教师信息
@app.route('/teacherMessage')
def teacherMessage():
    db = open_database()
    Message = get_teacherMessage_of(db)
    return render_template('teacherMessage.html', Message=Message)

#删除教师信息
@app.route('/delete_teacherMessage', methods=['GET', 'POST'])
def delete_teacherMessage():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('/'))
    teacher_id = request.form.get('teacher_id', '').strip()
    teacher_name = request.form.get('teacher_name', '').strip()
    complaint = None
    if request.method == 'POST':
        if teacher_id and teacher_name and teacher_id.isdigit():
            db = open_database()
            delete_teacherMessage(db, teacher_id, teacher_name)
            db.commit()
            return redirect(url_for('delete_teacherMessage', flash='send successful'))
        complaint = ('username must be text' if not teacher_id.isdigit()
                     else 'Please fill in all three fields')
    return get('delete_teacherMessage.html').render(complaint=complaint, teacher_id=teacher_id,
        teacher_name=teacher_name)




#添加课程信息
@app.route('/course', methods=['GET', 'POST'])
def course():
    course_id = request.form.get('course_id','').strip()
    course_name = request.form.get('course_name', '').strip()
    course_teacher = request.form.get('course_teacher', '').strip()
    course_title = request.form.get('course_title', '').strip()
    complaint = None
    if request.method == 'POST':
        if course_id and course_name and course_id.isdigit():
            db = open_database()
            add_courseMessage(db, course_id, course_name, course_teacher, course_title)
            db.commit()
            return redirect(url_for('course', flash='send successful'))
        complaint = ('课程名必须是数字' if not course_id.isdigit()
            else 'Please fill in all three fields')
    return get('course.html').render(complaint=complaint, course_id=course_id,
        course_name=course_name, course_teacher=course_teacher, course_title=course_title)

#显示课程信息
@app.route('/courseMessage')
def courseMessage():
    db = open_database()
    Message = get_courseMessage_of(db)
    return render_template('courseMessage.html', Message=Message)

#删除课程信息
@app.route('/delete_courseMessage', methods=['GET', 'POST'])
def delete_courseMessage():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('/'))
    course_id = request.form.get('course_id', '').strip()
    complaint = None
    if request.method == 'POST':
        if teacher_id and teacher_name and teacher_id.isdigit():
            db = open_database()
            delete_courseMessage(db, course_id)
            db.commit()
            return redirect(url_for('delete_courseMessage', flash='send successful'))
        complaint = ('username must be text' if not course_id.isdigit()
                     else 'Please fill in all three fields')
    return get('delete_courseMessage.html').render(complaint=complaint, course_id=course_id)

    

if __name__ == '__main__':
    app.debug = True
    app.run()
