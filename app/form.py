from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.models import Student

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
    # password = PasswordField("Password", validators=[DataRequired()])
    # confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("SignUp")

    def validate_user(self,username):
        user = Student.query.filter_by(user_name=username.data).first()
        if user is not None:
            raise ValidationError('username đã được đăng ký')
    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('email đã được đăng ký')
