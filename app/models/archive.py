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
    created_at = DateTimeField(
        default=datetime.now, verbose_name="创建时间"
    )
    updated_at = DateTimeField(
        default=datetime.now, verbose_name="更新时间"
    )
