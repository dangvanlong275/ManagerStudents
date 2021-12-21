from datetime import datetime
from enum import unique
from operator import index
from app import db,login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship

 
class Student(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable = False)
    age = db.Column(db.Integer, nullable = True)
    address = db.Column(db.String(64), nullable = True)
    email = db.Column(db.String(120), index=True, unique=True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    active = db.Column(db.Boolean,  default=False)
 
    def __repr__(self):
        return '<User {}>'.format(self.name)   
    def __init__(self,name,age,address,email):
        self.name = name
        self.age = age
        self.address = address
        self.email = email
        self.active = 1
    def insert_data(self):
        db.session.add(self)
        db.session.commit()
    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    

@login.user_loader
def loader_id(id):
    return Student.query.get(int(id))

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable = False)
    name_teacher = db.Column(db.String(64), nullable = False)

    def __init__(self,name,name_teacher):
        self.name = name
        self.age = name_teacher
    def insert_data(self):
        db.session.add(self)
        db.session.commit()
    def list_class():
        return Class.query.all()
    
class DetailStudent(db.Model):
    student_id = db.Column(db.Integer,primary_key=True)
    class_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP,default=datetime.utcnow, nullable = False)
    __table_args__ = (
        db.ForeignKeyConstraint(['student_id'], ['student.id'], name='fk_student_detail_student'),
        db.ForeignKeyConstraint(['class_id'], ['class.id'], name='fk_class_detail_student')
    )

    def __init__(self,student_id,class_id):
        self.student_id = student_id
        self.class_id = class_id
    def insert_data(self):
        db.session.add(self)
        db.session.commit()
class Admin(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), nullable = False)
    password = db.Column(db.String(64), nullable = False)
    def check_password(self, password):
        return check_password_hash(self.password, password)

@login.user_loader
def loader_id(id):
    return Admin.query.get(int(id))