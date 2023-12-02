from flask import Blueprint, render_template, request
from .models import Post

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
    print(post_id)
    post = Post.query.get(post_id)
    return render_template('post.html', **locals())
