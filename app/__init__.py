from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from config import config
from .models import DB, init_db, admin


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    """
    加载用户
    :param user_id: 用户ID
    :return: 用户对象
    """
    return admin.Admin.select().where(admin.Admin.id == int(user_id)).first()


login_manager.login_view = "auth.login"
login_manager.login_message = "请先登录"
login_manager.login_message_category = "info"


def create_app(config_name="default"):
    """
    Flask应用的工厂函数。
    :param config_name: 配置名称
    :return: Flask应用实例
    """
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])

    # 注册扩展（如数据库、登录管理等）
    Bootstrap5(app)
    app.config["BOOTSTRAP_SERVE_LOCAL"] = True
    app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "zephyr"
    login_manager.init_app(app)
    CKEditor(app)
    app.config["CKEDITOR_SERVE_LOCAL"] = True
    app.config["CKEDITOR_PKG_TYPE"] = "full"
    from peewee import PostgresqlDatabase, SqliteDatabase

    # 初始化数据库
    DB = None
    if config_name == "development" or config_name == "default":
        DB = SqliteDatabase(app.config["DB_URL"])
    else:
        # DB=PostgresqlDatabase(app.config["DB_URL"])
        pass
    init_db(DB)
    # 注册蓝图
    from .routes import blueprints

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
