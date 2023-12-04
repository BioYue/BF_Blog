from flask import Blueprint, render_template, request
from .models import Post
from start import db

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

    return render_template('post.html', **locals())
