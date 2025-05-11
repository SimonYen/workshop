from flask import Blueprint, render_template

# 创建蓝图实例
main_bp = Blueprint("main", __name__)


# 定义路由
@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")
