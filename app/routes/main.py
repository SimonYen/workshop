from flask import Blueprint, render_template, send_from_directory, request, url_for
from flask_ckeditor import upload_fail, upload_success
from app.utils.secure_filename import secure_filename

# 创建蓝图实例
main_bp = Blueprint("main", __name__)


# 定义路由
@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/ck_files/<path:filename>")
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
