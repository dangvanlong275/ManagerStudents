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

@app.route('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/profile')
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = ('/profile')
        return redirect(next_page)
    return render_template('login.html',title="Sign In Student", admin = False,form = form)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginFormAdmin()
    if current_user.is_authenticated:
        return redirect('/list-student')
    if form.validate_on_submit():
        user = Admin.query.filter_by(user_name=form.user_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/admin/login')
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = ('/list-student')
        return redirect(next_page)
    return render_template('login.html',title="Admin Login",admin = True,form = form)

@app.route('/register-student', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = Student(form.name.data, form.age.data, form.address.data, form.email.data)
        user.set_password("123456")
        user.insert_data()
        flash('Đăng ký thành công sinh viên')
        return redirect('/list-student')
    return render_template('register.html', title='Register Studentss', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route('/admin/logout')
def logout_admin():
    logout_user()
    return redirect('/admin/login')






