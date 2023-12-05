from flask import Blueprint, render_template, request, url_for
from .models import Post, Comment
from start import db
from .static.ip2region import search_with_file

# 实例化蓝图
bp = Blueprint('blog', __name__, url_prefix='/blog', template_folder='templates', static_folder='static')


def index():
    return render_template('index.html')


@bp.route('/post/<int:post_id>')
def post(post_id):
    """
    文章详情页
    :return:
    """
    post = Post.query.get(post_id)

    if post is None:
        return '404'
    post.read_count += 1
    db.session.commit()

    prev_post = Post.query.filter(Post.id < post.id).order_by(Post.id.desc()).first()
    next_post = Post.query.filter(Post.id > post.id).first()
    prev_post = prev_post if prev_post else None
    next_post = next_post if next_post else None

    comments = post.comments

    return render_template('post.html', **locals())


@bp.route('/comment_add', methods=['post'])
def comment_add():
    """
    添加评论
    :return:
    """
    form_data = request.form
    visitor_ip = request.remote_addr
    visitor_address = search_with_file(visitor_ip)
    comment = Comment(
        content=form_data['comment'],
        visitor_name=form_data['name'],
        visitor_email=form_data['email'],
        visitor_ip=visitor_ip,
        visitor_address=visitor_address,
        post_id=form_data['post_id']
    )
    db.session.add(comment)
    db.session.commit()
    return 'ok'


@bp.route('/comment_get')
def comment_get():
    """
    获取评论
    :return:
    """
    return 'ok'
