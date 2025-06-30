from flask import (
    Blueprint,
    render_template,
    send_from_directory,
    request,
    url_for,
    flash,
    redirect,
)
from flask_login import login_required
from flask_ckeditor import upload_fail, upload_success
from app.utils.secure_filename import secure_filename
from app.models.post import Post
from app.models.archive import Archive
from app.utils.weather import WeatherNow
from app.utils.list_files import get_files_in_filebin

# 创建蓝图实例
main_bp = Blueprint("main", __name__)


# 定义路由
@main_bp.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        f = request.files.get("file")
        if f:
            f.save(f"app/static/filebin/{f.filename}")
            flash(f"{f.filename}保存成功", "success")
        else:
            flash("文件为空！", "warning")
    # 获得数据库里帖子数量
    post_count = Post.select().count()
    archive_count = Archive.select().count()
    # 获取当前天气信息
    weather_now = None
    # filebin存储的文件
    file_list = get_files_in_filebin()
    try:
        weather_now = WeatherNow("101250109")  # 长沙市岳麓区
        weather_now.fetch_weather()
        weather_now.fetch_warning()
    except Exception as e:
        flash(f"获取信息失败: {e}", "warning")
    return render_template(
        "home.html",
        weather=weather_now,
        post_count=post_count,
        archive_count=archive_count,
        file_list=file_list,
    )


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/filebin/download/<path:filename>")
@login_required
def filebin_download(filename):
    from pathlib import Path

    root = Path(".")
    folder = root / "static/filebin"
    return send_from_directory(folder, filename)


@main_bp.route("/filebin/<path:filename>")
@login_required
def filebin_delete(filename):
    """
    删除文件
    :param filename: 文件名
    :return: 重定向到主页
    """

    import os

    file_path = f"app/static/filebin/{filename}"
    if os.path.exists(file_path):
        os.remove(file_path)  # 删除文件
        flash(f"{filename} 删除成功", "success")
    else:
        flash(f"{filename} 不存在", "warning")
    return redirect(url_for("main.home"))


@main_bp.route("/static/blog/ck/<path:filename>")
@login_required
def ck_files(filename):
    """
    处理CKEditor上传的文件
    :param filename: 文件名
    :return: 返回文件
    """

    from pathlib import Path

    root = Path(".")
    folder = root / "static/blog/ck"
    return send_from_directory(folder, filename)


@main_bp.route("/ck_upload", methods=["POST"])
@login_required
def ck_upload():
    """
    处理CKEditor上传的文件
    :return: 返回上传结果
    """
    if request.method == "POST":
        # 获取上传的文件
        file = request.files.get("upload")
        if file:
            # 保存文件
            filename = file.filename
            # 检查文件类型
            if not filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
                return upload_fail("只支持PNG、JPG、JPEG和GIF格式的图片")
            # 检查文件大小
            if file.content_length > 30 * 1024 * 1024:
                return upload_fail("文件大小超过限制，请上传小于30MB的文件")
            # 生成GUID文件名
            filename = secure_filename(filename)
            file.save(f"app/static/blog/ck/{filename}")
            # 返回成功信息
            return upload_success(url_for("main.ck_files", filename=filename))
        else:
            # 返回失败信息
            return upload_fail("上传失败，请重试")
    else:
        # 返回失败信息
        return upload_fail("上传失败，请重试")


@main_bp.route("/search")
def search():
    """
    搜索功能
    :return: 返回搜索结果页面
    """
    query = request.args.get("query", "")
    if not query:
        flash("请输入搜索内容", "warning")
        return redirect(url_for("main.home"))

    # 先找文章
    posts = Post.select().where(
        Post.title.contains(query) | Post.content.contains(query)
    )
    # 再找存档
    archives = Archive.select().where(
        Archive.title.contains(query) | Archive.summary.contains(query)
    )
    return render_template(
        "search_results.html", query=query, posts=posts, archives=archives
    )
