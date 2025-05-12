from flask import Blueprint, render_template, url_for, redirect, flash
from app.forms.login import LoginForm
from app.models.admin import Admin

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 从数据库中查询
        user = Admin.select().where(Admin.username == form.username.data).first()
        print(user)
        print(form.username.data)
        if user is None:
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))
        if user.password != form.password.data:
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))
        # 登录成功
        flash("Login successful", "success")
        return redirect(url_for("main.home"))
    return render_template("login.html", form=form)
