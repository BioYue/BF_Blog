from start import db
from datetime import datetime
from flask_login import UserMixin


class BaseModel(db.Model):
    """ 基类模型 """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, comment='id主键')
    add_time = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    upd_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), comment='更新时间')


class User(UserMixin, BaseModel):
    """ 用户模型 """
    __tablename__ = 'user_db'
    username = db.Column(db.String(64), unique=True, comment='用户名')
    password = db.Column(db.String(128), comment='密码')
    last_login = db.Column(db.DateTime, comment='上次登录时间')
    nickname = db.Column(db.String(64), comment='昵称')
    avatar_path = db.Column(db.String(256), comment='头像路径')
    posts = db.relationship('Post', backref='user')
    notes = db.relationship('Note', backref='user')


class BlogInfo(BaseModel):
    """ 网站信息 """
    __tablename__ = 'blogInfo_db'
    title = db.Column(db.String(64), comment='网站标题')
    subtitle = db.Column(db.String(64), comment='网站副标题')
    about_me = db.Column(db.Text, comment='关于我')
