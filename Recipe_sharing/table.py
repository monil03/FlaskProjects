from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime,timedelta


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///receipe.db"

db=SQLAlchemy(app)

class users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    post_receipe=db.relationship('post_receipe',backref="users",lazy=True)

class post_receipe(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    post_title=db.Column(db.String(100),nullable=False)
    post_description=db.Column(db.String(5000),nullable=False)
    image=db.Column(db.LargeBinary)
    likes=db.Column(db.Integer,default=0,nullable=False)
    comment=db.relationship('comments',backref="post_receipe",lazy=True)

class comments(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    user_name =db.Column(db.String(50),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    post_id=db.Column(db.Integer,db.ForeignKey('post_receipe.id'),nullable=False)
    comment=db.Column(db.String(5000),nullable=False)
    date=db.Column(db.DateTime,default=datetime.now)


class likes(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    post_receipe_id=db.Column(db.Integer,db.ForeignKey('post_receipe.id'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    like=db.Column(db.Integer,default=0,nullable=False)
