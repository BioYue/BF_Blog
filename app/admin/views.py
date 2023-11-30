import os.path

from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify
from .models import User
from app.blog.models import Category, Tag, Post, Attachment
from start import db
import json
from start.settings import BASE_DIR

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


@bp.route('/post')
def post():
    """
    文章管理-首页
    :return:
    """
    return render_template('admin/post.html')


@bp.route('/editor_post')
def editor_post():
    """
    文章管理-编辑文章页
    :return:
    """
    category_list = Category.query.all()
    tag_list = Tag.query.all()
    return render_template('admin/editor_post.html', **locals())


@bp.route('/post_add', methods=['post'])
def post_add():
    """
    文章管理-新增文章API
    :return:
    """
    form_data = request.form
    tags = json.loads(form_data['tags'])
    tags_obj = [Tag.query.get(tag_id) for tag_id in list(tags.keys())]

    post_obj = Post(
        title=form_data['title'],
        content_md=form_data['markdown'],
        content_html=form_data['html'],
        category_id=form_data['category'],
        tags=tags_obj,
        cover=form_data['cover']
    )

    img_ids = [i['id'] for i in json.loads(form_data['img_list'])]
    attachments = Attachment.query.filter(Attachment.id.in_(img_ids)).all()
    post_obj.attachments.extend(attachments)

    db.session.add(post_obj)
    db.session.commit()
    return 'success'


@bp.route('/post_query')
def post_query():
    """
    文章管理-查询文章API
    :return:
    """
    page = request.args.get('page', type=int, default=1)  # 当前页
    limit = request.args.get('limit', type=int, default=10)  # 一页条数
    post_pg = Post.query.paginate(page=page, per_page=limit)

    post_list = []
    for item in post_pg.items:
        row = {
            'id': item.id,
            'title': item.title,
            'read_count': item.read_count,
            'category': item.category.name,
            'add_time': item.add_time.strftime("%Y-%m-%d"),
            'upd_time': item.upd_time.strftime("%Y-%m-%d")
        }
        post_list.append(row)

    data = {
        'code': 0,
        'data': post_list,  # 实际数据
        'count': post_pg.total,  # 数据总数
        'msg': ''
    }
    return jsonify(data)


@bp.route('/upload', methods=['post'])
def upload():
    """
    文章管理-资源上传API
    :return:
    """
    file = request.files.get('file')
    name = request.form.get('name')
    size = request.form.get('size')
    file_path = f'app/blog/static/upload/{name}'
    file.save(BASE_DIR / file_path)
    attachment = Attachment(file_name=name, file_size=size, file_path=file_path)
    db.session.add(attachment)
    db.session.commit()
    return {'id': attachment.id, 'url': url_for('blog.static', filename=f'upload/{name}')}


@bp.route('/category')
def category():
    """
    分类管理-首页
    :return:
    """
    return render_template('admin/category.html', **locals())


@bp.route('/category_add', methods=['post'])
def category_add():
    """
    分类管理-新增分类API
    :return:
    """
    category_name = request.form['value']
    category_ = Category.query.filter_by(name=category_name).first()
    if not category_:
        category_obj = Category(name=category_name)
        db.session.add(category_obj)
        db.session.commit()
        return 'success'
    return 'existed'


@bp.route('/category_query')
def category_query():
    """
    分类管理-查询分类API
    :return:
    """
    page = request.args.get('page', type=int, default=1)  # 当前页
    limit = request.args.get('limit', type=int, default=5)  # 一页条数
    category_pg = Category.query.paginate(page=page, per_page=limit)
    category_list = []
    for item in category_pg.items:
        row = {
            'id': item.id,
            'name': item.name,
            'add_time': item.add_time.strftime("%Y-%m-%d"),
            'upd_time': item.upd_time.strftime("%Y-%m-%d")
        }
        category_list.append(row)
    # layui需要的表格数据解析回调的格式
    data = {
        'code': 0,
        'data': category_list,  # 实际数据
        'count': category_pg.total,  # 数据总数
        'msg': ''
    }
    return jsonify(data)


@bp.route('/tag')
def note():
    """
    标签管理-首页
    :return:
    """
    return render_template('admin/tag.html')


@bp.route('/tag_add', methods=['post'])
def tag_add():
    """
    标签管理-新增标签API
    :return:
    """
    tag_name = request.form['tag_name']
    tag_color = request.form['tag_color']
    print(tag_name)
    tag_ = Tag.query.filter_by(name=tag_name).first()
    if not tag_:
        tag_obj = Tag(name=tag_name, color=tag_color)
        db.session.add(tag_obj)
        db.session.commit()
        return 'success'
    return 'existed'


@bp.route('/tag_query')
def tag_query():
    """
    标签管理-查询标签API
    :return:
    """
    page = request.args.get('page', type=int, default=1)  # 当前页
    limit = request.args.get('limit', type=int, default=5)  # 一页条数
    tag_pg = Tag.query.paginate(page=page, per_page=limit)
    tag_list = []
    for item in tag_pg.items:
        row = {
            'id': item.id,
            'name': item.name,
            'color': item.color,
            'add_time': item.add_time.strftime("%Y-%m-%d"),
            'upd_time': item.upd_time.strftime("%Y-%m-%d")
        }
        tag_list.append(row)
    # layui需要的表格数据解析回调的格式
    data = {
        'code': 0,
        'data': tag_list,  # 实际数据
        'count': tag_pg.total,  # 数据总数
        'msg': ''
    }
    return jsonify(data)


@bp.route('/test_url')
def test_url():
    html = Post.query.get(8).content_html
    print(html)
    return render_template('admin/test.html', **locals())
