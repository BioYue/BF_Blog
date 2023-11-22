from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# 实例化SQLAlchemy对象
db = SQLAlchemy()
# 实例化迁移对象
migrate = Migrate()
# 实例化login管理
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # 注册配置文件
    app.config.from_pyfile('settings.py')

    # 引入blog视图(这个引入必须放在create_app里)
    from app.blog import views as blog
    # 注册blog蓝图
    app.register_blueprint(blog.bp)

    # 注册数据库
    db.init_app(app)
    # 注册迁移对象
    migrate.init_app(app, db)
    # 注册login管理
    # login_manager.init_app(app)

    # 注册模型
    from app.blog import models
    from app.admin import models

    # 注册首页url规则
    app.add_url_rule(rule='/', endpoint='index', view_func=blog.index)
    return app
