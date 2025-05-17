from peewee import *
from . import BaseModel
from .post import Post


class Archive(BaseModel):
    """
    归档模型类
    """

    id = PrimaryKeyField(verbose_name="ID")
    title = CharField(verbose_name="标题", unique=True)
    summary = TextField(verbose_name="摘要")
    post = ForeignKeyField(Post, backref="archives", verbose_name="帖子")
    created_at = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], verbose_name="创建时间"
    )
    updated_at = DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], verbose_name="更新时间"
    )
