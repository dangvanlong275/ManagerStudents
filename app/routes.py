from flask.helpers import flash
from flask_login.utils import logout_user
from sqlalchemy.sql.expression import null, select
from werkzeug.utils import redirect
from app import app, db
from flask import render_template, sessions
from app.form import LoginForm, LoginFormAdmin, RegisterForm
from flask_login import current_user, login_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.models import DetailStudent, Student,Admin,Class

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Long'}
    
    posts = [
        {
            'author': {'username': 'Nguyen'},
            'body': 'Flask de hoc qua phai khong?'
        },
        {
            'author': {'username': 'Long'},
            'body': 'Lap trinh Web that thu vi!'
        }
    ]
    return render_template('index.html', title='Home', user=user,posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/index')
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = ('/index')
        return redirect(next_page)
    return render_template('login.html',title="Sign In Student", admin = False,form = form)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginFormAdmin()
    if current_user.is_authenticated:
        return redirect('/index')
    if form.validate_on_submit():
        user = Admin.query.filter_by(user_name=form.user_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = ('/index')
        return redirect(next_page)
    return render_template('login.html',title="Admin Login",admin = True,form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect('/index')
    if form.validate_on_submit():
        user = Student(form.name.data, form.age.data, form.address.data, form.email.data)
        user.set_password("123456")
        user.insert_data()
        flash('Đăng ký thành công, hệ thống sẽ tự động đăng nhập')
        login_user(user)
        return redirect('/index')
    return render_template('register.html', title='Register Studentss', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
@app.route('/list-class')
@login_required
def class_manager():
    list_class = Class.query.all()
    user = Student.query.get(current_user.id)
    return render_template('class_view.html',title="List class",user=user,list_class=list_class)
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
@app.route('/profile', methods =['GET', 'POST'])
@login_required
def profile():
    user = Student.query.get(current_user.id)
    return render_template('index.html', title='Home', user=user,posts = null)