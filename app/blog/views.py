from flask import Blueprint, render_template
from .models import Post

# 实例化蓝图
bp = Blueprint('blog', __name__, url_prefix='/blog', template_folder='templates', static_folder='static')


@bp.route('/index')
def index():
    # post = Post.query.get(1)
    return 'ok'
    # return render_template('index.html', post=post.__dict__)
