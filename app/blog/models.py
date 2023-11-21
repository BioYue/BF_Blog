from start import db
from datetime import datetime

"""多对多中间表"""
# 文章与标签多对多中间表
post_tag = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post_db.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag_db.id'), primary_key=True)
)
# 笔记与标签多对多中间表
note_tag = db.Table(
    'note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('note_db.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag_db.id'), primary_key=True)
)


class BaseModel(db.Model):
    """ 基类模型 """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, comment='id主键')
    add_time = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    upd_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), comment='更新时间')


class Post(BaseModel):
    """ 文章模型 """
    __tablename__ = 'post_db'
    title = db.Column(db.String(256), comment='标题')
    cover = db.Column(db.String(512), comment='文章封面')
    content_md = db.Column(db.Text, comment='markdown源内容')
    content_html = db.Column(db.Text, comment='html内容')
    read_count = db.Column(db.Integer, default=0, comment='阅读次数')
    draft_flag = db.Column(db.Boolean, default=False, comment='是否为草稿')
    category_id = db.Column(db.Integer, db.ForeignKey('category_db.id'), comment='分类id')
    tags = db.relationship('Tag', secondary=post_tag, backref='posts')
    comments = db.relationship('Comment', backref='post', cascade='delete')
    attachments = db.relationship('Attachment', backref='post')
    user_id = db.Column(db.Integer, db.ForeignKey('user_db.id'), comment='用户id')


class Category(BaseModel):
    """ 分类表 """
    __tablename__ = 'category_db'
    name = db.Column(db.String(64), unique=True, comment='分类名')
    posts = db.relationship('Post', backref='category')
    notes = db.relationship('Note', backref='category')


class Tag(BaseModel):
    """ 标签表 """
    __tablename__ = 'tag_db'
    name = db.Column(db.String(64), unique=True, comment='标签名')
    color = db.Column(db.String(32), comment='标签颜色')


class Note(BaseModel):
    """ 笔记表 """
    __tablename__ = 'note_db'
    title = db.Column(db.String(256), comment='标题')
    content_md = db.Column(db.Text, comment='markdown源内容')
    content_html = db.Column(db.Text, comment='html内容')
    read_count = db.Column(db.Integer, default=0, comment='阅读次数')
    category_id = db.Column(db.Integer, db.ForeignKey('category_db.id'), comment='分类id')
    tags = db.relationship('Tag', secondary=note_tag, backref='note')
    attachments = db.relationship('Attachment', backref='note')
    user_id = db.Column(db.Integer, db.ForeignKey('user_db.id'), comment='用户id')


class Comment(BaseModel):
    """ 评论表 """
    __tablename__ = 'comment_db'
    content = db.Column(db.Text, comment='评论内容')
    visitor_name = db.Column(db.String(64), comment='游客名')
    visitor_email = db.Column(db.String(64), comment='游客邮箱')
    visitor_ip = db.Column(db.String(50), comment='游客ip')
    visitor_address = db.Column(db.String(50), comment='游客地址')
    post_id = db.Column(db.Integer, db.ForeignKey('post_db.id'), comment='文章id')
    replied_id = db.Column(db.Integer, db.ForeignKey('comment_db.id'), comment='回复属于某一条评论')
    replied = db.relationship('Comment', back_populates='replies', remote_side='Comment.id')
    replies = db.relationship('Comment', back_populates='replied', cascade='delete')


class Message(BaseModel):
    """ 留言表 """
    __tablename__ = 'message_db'
    content = db.Column(db.Text, comment='评论内容')
    visitor_name = db.Column(db.String(64), comment='游客名')
    visitor_email = db.Column(db.String(64), comment='游客邮箱')
    visitor_ip = db.Column(db.String(50), comment='游客ip')
    visitor_address = db.Column(db.String(50), comment='游客地址')


class Attachment(BaseModel):
    """ 附件表 """
    __tablename__ = 'attachment_db'
    file_name = db.Column(db.String(512), comment='文件名')
    file_size = db.Column(db.String(32), comment='文件大小')
    file_path = db.Column(db.String(256), comment='文件路径')
    post_id = db.Column(db.Integer, db.ForeignKey('post_db.id'), comment='文章id')
    note_id = db.Column(db.Integer, db.ForeignKey('note_db.id'), comment='笔记id')
