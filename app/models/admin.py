from . import BaseModel
from peewee import *

class Admin(BaseModel):
	"""
	管理员模型类
	"""
	id=PrimaryKeyField(verbose_name="ID")
	username = CharField(unique=True, verbose_name="用户名")
	password = CharField(verbose_name="密码")
