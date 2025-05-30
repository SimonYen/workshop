from peewee import *
from . import BaseModel
from .admin import Admin
from datetime import datetime

class Post(BaseModel):
    """
    帖子模型类
    """

    id = PrimaryKeyField(verbose_name="ID")
    title = CharField(verbose_name="标题", unique=True)
    cover = CharField(verbose_name="封面", null=True)
    summary = CharField(verbose_name="摘要", null=True)
    is_top = BooleanField(default=False, verbose_name="置顶")
    background = CharField(verbose_name="背景", null=True)
    content = TextField(verbose_name="内容")
    author = ForeignKeyField(Admin, backref="posts", verbose_name="作者")
    tags = CharField(verbose_name="标签", null=True)
    created_at = DateTimeField(
        default=datetime.now, verbose_name="创建时间"
    )
    updated_at = DateTimeField(
        default=datetime.now, verbose_name="更新时间"
    )

    class Meta:
        # 这里的索引是为了加快查询速度
        indexes = ((("title",), True),)
