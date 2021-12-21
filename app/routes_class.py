from flask.helpers import flash
from flask_login.utils import logout_user
from sqlalchemy.orm import query
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


@app.route('/list-class')
@login_required
def class_manager():
    list_class = Class.query.all()
    user = Student.query.get(current_user.id)
    return render_template('class_view.html',title="List class",user=user,list_class=list_class)

@app.route('/create-class', methods=['GET','POST'])
@login_required
def create_class():
    form = CreatedClass()
    if request.method == 'POST':
        class_ = Class(form.name.data, form.teacher_name.data)
        class_.insert_data()
        flash('Tạo lớp học thành công!')
        return redirect('/class')
    return render_template('manager_class.html', title='Manager Class', form=form)

@app.route('/detail-class', methods=['GET'])
@login_required
def detail_class():
    class_id_ = request.args.get("class_id")
    detail_class = Student.query.join(DetailStudent, Student.id==DetailStudent.student_id)\
                .filter(DetailStudent.class_id == class_id_)
    return render_template('detail_class.html',detail_class=detail_class)

@app.route('/search-class', methods=['GET'])
@login_required
def search_class():
    class_id = request.args.get("class_id")
    class_ = Class.query.get(class_id)
    return render_template('detail_class.html',detail_class=class_)

@app.route('/update-class', methods=['POST'])
@login_required
def update_class():
    class_id = request.form.get("class_id")
    name = request.form.get("name")
    teacher_name = request.form.get("teacher_name")

    class_ = Class.query.get(class_id)
    class_.update_data(name, teacher_name)
    return render_template('detail_class.html',detail_class=class_id)

@app.route('/delete-class', methods=['POST'])
@login_required
def delete_class():
    class_id_ = request.form.get("class_id")
    DetailStudent.query.filter_by(class_id = class_id_).delete()
    class_ = Class.query.filter_by(id = class_id_).one()
    class_.delete_class()
    return render_template('detail_class.html',detail_class=class_id_)
