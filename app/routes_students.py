from flask.helpers import flash
from flask_login.utils import logout_user
from sqlalchemy.sql.expression import null, select
from werkzeug.utils import redirect
from app import app, db
from flask import render_template, sessions
from app.form import CreatedClass, LoginForm, LoginFormAdmin, RegisterForm
from flask_login import current_user, login_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.models import DetailStudent, Student,Admin,Class


@app.route('/join-class', methods=['GET', 'POST'])
@login_required
def join_class():
    if request.method == 'POST':
        DetailStudent.query.filter_by(student_id=current_user.id).delete()
        regis_class = request.form.getlist('regis_class')
        for _class in regis_class:
            join_class = DetailStudent(current_user.id,_class)
            join_class.insert_data()
    user = Student.query.get(current_user.id)
    list_class_student = Class.query.join(DetailStudent, Class.id==DetailStudent.class_id)\
                .filter(DetailStudent.student_id == current_user.id)
    class_id = list_class_student.with_entities(DetailStudent.class_id)
    list_class = Class.query.join(DetailStudent, Class.id==DetailStudent.class_id, isouter = True)\
                .filter(Class.id.notin_(class_id))
    return render_template('class.html',title="Join Class",user=user, list_class=list_class,list_class_student=list_class_student)

@app.route('/profile', methods =['GET'])
@login_required
def profile():
    user = Student.query.get(current_user.id)
    return render_template('profile.html', title='Home', user=user)

@app.route('/list-student', methods=['GET'])
@login_required
def list_students():
    list_students = Student.list_student()
    return render_template('student_view.html',list_students=list_students)


@app.route('/update-student', methods=['POST'])
@login_required
def update_student():
    student_id = request.form.get("student_id")
    name = request.form.get('name')
    age = request.form.get('age')
    address = request.form.get('address')
    email = request.form.get('email')

    student = Student.query.get(student_id)
    student.update_student(name, age, address, email)
    return redirect('/profile')

@app.route('/update-activate-student', methods=['POST'])
@login_required
def update_activate_student():
    student_id = request.form.get("student_id")
    activate = request.form.get('activate')
    student = Student.query.get(student_id)
    student.update_active(activate)
    return render_template('detail_class.html',detail_class=student_id)

@app.route('/delete-student', methods=['POST'])
@login_required
def delete_students():
    student_id = request.form.get("student_id")
    student = Student.query.filter_by(id = student_id).one()
    student.delete_student()
    return redirect('/list-student')