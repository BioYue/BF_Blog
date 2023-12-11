from flask import Blueprint, render_template, request, url_for, jsonify
from sqlalchemy import func

from .models import Post, Comment, Message, Note
from app.admin.models import BlogInfo
from start import db
from .static.ip2region import search_with_file

# 实例化蓝图
bp = Blueprint('blog', __name__, url_prefix='/blog', template_folder='templates', static_folder='static')


@bp.route('/page/<int:curr>')
def index(curr=1):
    post_pg = Post.query.paginate(page=curr, per_page=5)
    count = post_pg.total
    return render_template('index.html', **locals())


@bp.route('/post_query', methods=['post'])
def post_query():
    page = request.args.get('page', type=int, default=1)  # 当前页
    limit = request.args.get('limit', type=int, default=5)  # 一页条数
    post_pg = Post.query.paginate(page=page, per_page=limit)

    post_list = []
    for item in post_pg.items:
        row = {
            'id': item.id,
            'title': item.title,
            'cover': item.cover,
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

    main_comments = Comment.query.filter_by(post_id=post_id, replied_id=None).order_by(Comment.add_time.desc()).all()
    all_comments = []
    for main_comment in main_comments:
        replies = get_replies(comment_id=main_comment.id)
        replies = sorted(replies, key=lambda x: x['add_time'], reverse=True)
        comment_data = {
            'id': main_comment.id,
            'content': main_comment.content,
            'visitor_name': main_comment.visitor_name,
            'visitor_address': main_comment.visitor_address,
            'add_time': main_comment.add_time,
            'replies': replies
        }
        all_comments.append(comment_data)

    return render_template('post.html', **locals())


def get_replies(comment_id, reply_target_name=None):
    # 获取特定评论的所有子评论
    replies = Comment.query.filter_by(replied_id=comment_id).all()

    # 递归处理子评论的子评论
    reply_data = []
    for reply in replies:
        reply_data.append({
            'id': reply.id,
            'content': reply.content,
            'visitor_name': reply.visitor_name,
            'add_time': reply.add_time,
            'visitor_address': reply.visitor_address,
            'reply_target_name': reply_target_name,
        })
        reply_data.extend(get_replies(reply.id, reply.visitor_name))
    return reply_data


@bp.route('/comment_add', methods=['post'])
def comment_add():
    """
    添加评论-API
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
    return 'success'


@bp.route('/comment_reply', methods=['post'])
def comment_reply():
    """
    评论回复-API
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
        post_id=form_data['post_id'],
        replied_id=form_data['replied_id']
    )
    db.session.add(comment)
    db.session.commit()
    return 'success'


@bp.route('/record')
def record():
    """
    归档页面
    :return:
    """
    posts = Post.query.filter_by(draft_flag=False).order_by(Post.add_time.desc()).all()
    record_list = {}
    for post in posts:
        date = str(post.add_time.strftime("%Y-%m"))
        record_list.setdefault(date, []).append(post)

    return render_template('record.html', **locals())


@bp.route('/note/<int:curr>')
@bp.route('/note')
def note(curr=1):
    """
    笔记页面
    :return:
    """
    note_pg = Note.query.paginate(page=curr, per_page=5)
    count = note_pg.total
    return render_template('note.html', **locals())


@bp.route('/message')
def message():
    """
    留言页面
    :return:
    """
    messages = Message.query.order_by(Message.add_time.desc()).all()
    return render_template('message.html', **locals())


@bp.route('/message_add', methods=['post'])
def message_add():
    """
    留言添加-API
    :return:
    """
    form_data = request.form
    visitor_ip = request.remote_addr
    visitor_address = search_with_file(visitor_ip)
    message = Message(
        content=form_data['comment'],
        visitor_name=form_data['name'],
        visitor_email=form_data['email'],
        visitor_ip=visitor_ip,
        visitor_address=visitor_address,
    )
    db.session.add(message)
    db.session.commit()
    return 'success'


@bp.route('/about')
def about():
    """
    关于页面
    :return:
    """
    bloginfo = BlogInfo.query.first()
    about_me_html = bloginfo.about_me_html
    return render_template('about.html', **locals())
