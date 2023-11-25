from flask import Blueprint, render_template
from .models import User

# 实例化蓝图
bp = Blueprint('admin', __name__, url_prefix='/bf_admin', template_folder='templates', static_folder='static')


# 后台登录页
@bp.route('/login')
def login():
    return '后台登录页'


# 后台首页
@bp.route('/')
def index():
    return render_template('admin/index.html')


# 文章管理页
@bp.route('/post')
def post():
    return render_template('admin/post.html')
