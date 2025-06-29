from peewee import *
from . import BaseModel
from datetime import datetime


class Archive(BaseModel):
    """
    归档模型类
    """

    id = PrimaryKeyField(verbose_name="ID")
    title = CharField(verbose_name="标题", unique=True)
    summary = TextField(verbose_name="摘要")
    created_at = DateTimeField(default=datetime.now, verbose_name="创建时间")
    updated_at = DateTimeField(default=datetime.now, verbose_name="更新时间")
    # 关联的帖子
    posts = []

    class Meta:
        # 这里的索引是为了加快查询速度
        indexes = ((("title",), True),)

    # 重载save方法
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(Archive, self).save(*args, **kwargs)
