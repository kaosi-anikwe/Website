from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import ForeignKey, Boolean
from flaskr import db


class Users(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DATE, default=datetime.now())
    status = db.Column(db.Boolean, default=False, nullable=False)
    account = db.Column(db.String(12), default='student', nullable=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()


class Courses(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(1000), nullable=False)
    requirements = db.Column(db.String(2000), nullable=False)
    duration = db.Column(db.String(50))
    progress = db.Column(db.Integer, nullable=False)
    lectures = db.Column(db.Integer, nullable=False)
    quizzes = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, ForeignKey('course.id'))
    user = db.relationship("User", backref=db.backref("user", uselist=False))

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Enrolled(db.Model):
    __tablename__ = "enrolled"
    id = db.Column(db.Integer, primary_key=True)
    enrollment = db.Column(db.Boolean, nullable=False)
    student_id = db.Column(db.Integer, ForeignKey('user.id'))
    course_id = db.Column(db.Integer, ForeignKey('course.id'))
    course = db.relationship("Course", backref=db.backref("course"))
