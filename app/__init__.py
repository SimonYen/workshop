from flask import Flask
from flask_bootstrap import Bootstrap5
from config import config


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
    bootstrap = Bootstrap5(app)
    app.config["BOOTSTRAP_SERVE_LOCAL"] = True
    app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "flatly"
    # from .extensions import db, login_manager
    # db.init_app(app)
    # login_manager.init_app(app)

    # 注册蓝图
    from .routes import blueprints

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
