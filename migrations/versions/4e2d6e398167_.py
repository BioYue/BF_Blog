"""empty message

Revision ID: 4e2d6e398167
Revises: 6ff03966dd6d
Create Date: 2023-12-08 16:13:42.102550

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4e2d6e398167'
down_revision = '6ff03966dd6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogInfo_db',
    sa.Column('title', sa.String(length=64), nullable=True, comment='网站标题'),
    sa.Column('subtitle', sa.String(length=64), nullable=True, comment='网站副标题'),
    sa.Column('about_me_mk', sa.Text(), nullable=True, comment='关于我mk格式'),
    sa.Column('about_me_html', sa.Text(), nullable=True, comment='关于我html格式'),
    sa.Column('id', sa.Integer(), nullable=False, comment='id主键'),
    sa.Column('add_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('upd_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('bloginfo_db')
    with op.batch_alter_table('message_db', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=mysql.TEXT(),
               comment='留言内容',
               existing_comment='评论内容',
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message_db', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=mysql.TEXT(),
               comment='评论内容',
               existing_comment='留言内容',
               existing_nullable=True)

    op.create_table('bloginfo_db',
    sa.Column('title', mysql.VARCHAR(length=64), nullable=True, comment='网站标题'),
    sa.Column('subtitle', mysql.VARCHAR(length=64), nullable=True, comment='网站副标题'),
    sa.Column('about_me', mysql.TEXT(), nullable=True, comment='关于我'),
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False, comment='id主键'),
    sa.Column('add_time', mysql.DATETIME(), nullable=True, comment='创建时间'),
    sa.Column('upd_time', mysql.DATETIME(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('blogInfo_db')
    # ### end Alembic commands ###