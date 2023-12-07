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

    main_comments = Comment.query.filter_by(post_id=post_id, replied_id=None).order_by(Comment.add_time.desc()).all()
    all_comments = []
    for main_comment in main_comments:
        comment_data = {
            'id': main_comment.id,
            'content': main_comment.content,
            'visitor_name': main_comment.visitor_name,
            'visitor_address': main_comment.visitor_address,
            'add_time': main_comment.add_time,
            'replies': get_replies(comment_id=main_comment.id)
        }
        all_comments.append(comment_data)

    print(all_comments)

    return render_template('post.html', **locals())


def get_replies(comment_id, reply_target_name=None):
    # 获取特定评论的所有子评论
    replies = Comment.query.filter_by(replied_id=comment_id).order_by(Comment.add_time).all()

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


@bp.route('/comment_get')
def comment_get():
    """
    获取评论
    :return:
    """
    return 'ok'


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


@bp.route('/test')
def test():
    """
    测试
    :return:
    """
    comment = Comment.query.get(1)
    print(comment.replies)

    return 'ok'
