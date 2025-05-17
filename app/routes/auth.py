from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user
from app.forms.login import LoginForm
from app.models.admin import Admin

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 从数据库中查询
        user = Admin.select().where(Admin.username == form.username.data).first()
        if user is None:
            flash("用户名不存在！", "danger")
            return redirect(url_for("auth.login"))
        if user.password != form.password.data:
            flash("密码错误！", "danger")
            return redirect(url_for("auth.login"))
        # 登录成功
        flash("登陆成功", "success")
        login_user(user)
        return redirect(url_for("main.home"))
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
def logout():
    """
    处理用户登出请求
    :return: 重定向到主页
    """
    logout_user()
    flash("登出成功", "success")
    return redirect(url_for("main.home"))
