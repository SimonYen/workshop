import os
import uuid
from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    flash,
    request,
)
from flask_login import login_required, current_user
from app.forms.editor import BlogEditorForm
from app.models.post import Post

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@login_required
@admin_bp.route("/blog/index")
def blog_index():
    """
    博客管理首页
    :return: 渲染博客管理首页模板
    """
    # 获取请求页
    page = request.args.get("page", 1, type=int)
    # 定义每一页显示的博客数量
    per_page = 12
    # 计算总页数
    total_pages = (Post.select().count() + per_page - 1) // per_page
    if page > total_pages:
        page = total_pages
    # 获取所有博客
    posts = Post.select().order_by(Post.updated_at.desc()).paginate(page, per_page)
    # 前一页
    prev_page = page - 1 if page > 1 else None
    # 后一页
    next_page = page + 1 if page < total_pages else None
    # 渲染模板
    return render_template(
        "blog/index.html",
        posts=posts,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        current_page=page,
    )


@login_required
@admin_bp.route("/blog/create", methods=["GET", "POST"])
def blog_create():
    """
    创建博客
    :return: 渲染创建博客模板
    """
    form = BlogEditorForm()
    if form.validate_on_submit():
        # 处理表单提交
        post = Post.create(
            title=form.title.data,
            content=form.content.data,
            tags=form.tags.data,
            author_id=current_user.get_id(),
            summary=form.summary.data,
            is_top=form.is_top.data,
        )
        if post:
            flash("博客创建成功", "success")
        else:
            flash("博客创建失败", "danger")
        return redirect(url_for("admin.blog_index"))
    return render_template("blog/editor.html", form=form)

@login_required
@admin_bp.route("/blog/edit/<int:post_id>", methods=["GET", "POST"])
def blog_edit(post_id):
    """
    编辑博客
    :param post_id: 博客ID
    :return: 渲染编辑博客模板
    """
    post:Post = Post.get_or_none(Post.id == post_id)
    if not post:
        flash("博客不存在", "danger")
        return redirect(url_for("admin.blog_index"))
    form = BlogEditorForm()
    if request.method == "GET":
        # 填充表单数据
        form.title.data = post.title
        form.content.data = post.content
        form.tags.data = post.tags
        form.summary.data = post.summary
        form.is_top.data = post.is_top
    if form.validate_on_submit():
        # 处理表单提交
        post.title = form.title.data
        post.content = form.content.data
        post.tags = form.tags.data
        post.summary = form.summary.data
        post.is_top = form.is_top.data
        post.save()
        flash("博客更新成功", "success")
        return redirect(url_for("admin.blog_index"))
    return render_template("blog/editor.html", form=form, post=post)

@login_required
@admin_bp.route("/blog/delete/<int:post_id>")
def blog_delete(post_id):
    """
    删除博客
    :param post_id: 博客ID
    :return: 重定向到博客主页
    """
    post:Post = Post.get_or_none(Post.id == post_id)
    if not post:
        flash("博客不存在", "danger")
        return redirect(url_for("admin.blog_index"))
    if post.cover:
        try:
            os.remove(os.path.join("app/static/blog/cover", post.cover))
        except FileNotFoundError:
            pass
    # 删除博客
    post.delete_instance()
    flash("博客删除成功", "success")
    return redirect(url_for("admin.blog_index"))


@login_required
@admin_bp.route("/blog/cover/<int:post_id>", methods=["POST"])
def blog_cover(post_id):
    """
    上传博客封面
    :param post_id: 博客ID
    :return: 重定向到博客主页
    """
    post:Post = Post.get_or_none(Post.id == post_id)
    if not post:
        flash("博客不存在", "danger")
        return redirect(url_for("admin.blog_index"))
    # 取出封面文件
    f= request.files.get("cover")
    if not f:
        flash("请上传封面", "danger")
        return redirect(url_for("admin.blog_index"))
    # 检查文件类型
    if not f.filename.endswith((".png", ".jpg", ".jpeg")):
        flash("只支持PNG、JPG、JPEG格式的图片", "danger")
        return redirect(url_for("admin.blog_index"))
    # 检查文件大小
    if f.content_length > 30 * 1024 * 1024:
        flash("文件大小超过限制，请上传小于30MB的文件", "danger")
        return redirect(url_for("admin.blog_index"))
    # 生成GUID文件名
    filename = f"{uuid.uuid4()}{os.path.splitext(f.filename)[1]}"
    # 检查是否存在旧封面
    if post.cover:
        # 删除旧封面
        try:
            os.remove(os.path.join("app/static/blog/cover", post.cover))
        except FileNotFoundError:
            pass
    post.cover = filename
    post.save()
    # 保存新封面
    f.save(os.path.join("app/static/blog/cover", filename))
    # 返回成功消息
    flash(f"{post.title}封面上传成功", "success")
    return redirect(url_for("admin.blog_index"))