from flask_wtf import FlaskForm
from sqlalchemy.orm import query
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.models import Class, Student

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("SingIn")

class LoginFormAdmin(FlaskForm):
    user_name = StringField('User name', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("SingIn")

class RegisterForm(FlaskForm):
    name = StringField('UserName', validators=[DataRequired()])
    age = StringField("Age", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("SignUp")

    def validate_user(self,username):
        user = Student.query.filter_by(user_name=username.data).first()
        if user is not None:
            raise ValidationError('Username đã được đăng ký')
    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email đã được đăng ký')

class CreatedClass(FlaskForm):
    name = StringField('Class Name', validators=[DataRequired()])
    teacher_name = StringField("Teacher Name", validators=[DataRequired()])
    submit = SubmitField("Created")

    def validate_name(self, name):
        class_ = Class.query.filter_by(name = name.data).first()
        if class_ is not None:
            raise ValidationError('Lớp học đã tồn tại')