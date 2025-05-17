from peewee import *

DB = None


class BaseModel(Model):
    """
    基础模型类，所有模型都应该继承这个类。
    """

    class Meta:
        database = DB  # 使用全局数据库句柄


# 数据库初始化
def init_db(db):
    """
    初始化数据库
    :param db: 数据库句柄
    """
    global DB
    DB = db
    if DB is None:
        return
    # 设置所有模型的数据库
    from .admin import Admin
    from .post import Post
    from .archive import Archive

    Admin._meta.database = DB  # 显式设置 Admin 的数据库
    Post._meta.database = DB  # 显式设置 Post 的数据库
    Archive._meta.database = DB  # 显式设置 Archive 的数据库
    # 连接数据库
    DB.connect()
    # 创建表
    DB.create_tables([Admin, Post, Archive])
