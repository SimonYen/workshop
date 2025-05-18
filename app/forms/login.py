from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "用户名",
        validators=[
            InputRequired(message="请输入用户名"),
        ],
    )
    password = PasswordField(
        "密码",
        validators=[
            InputRequired(message="请输入密码"),
            Length(min=6, max=35, message="密码长度必须在6到35个字符之间"),
        ],
    )
    submit = SubmitField("登录")
