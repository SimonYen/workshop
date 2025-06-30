import os
from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    flash,
    request,
    send_file,
)
from flask_login import login_required, current_user
from bs4 import BeautifulSoup
from app.forms.editor import BlogEditorForm, ArchiveEditorForm
from app.models.post import Post
from app.models.archive import Archive
from app.utils.secure_filename import secure_filename
from app.utils.packageing import packaging_file

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/blog/index")
@login_required
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


@admin_bp.route("/blog/create", methods=["GET", "POST"])
@login_required
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
            archives=form.archives.data,
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


@admin_bp.route("/blog/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def blog_edit(post_id):
    """
    编辑博客
    :param post_id: 博客ID
    :return: 渲染编辑博客模板
    """
    post: Post = Post.get_or_none(Post.id == post_id)
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
        form.archives.data = post.archives
        form.is_top.data = post.is_top
    if form.validate_on_submit():
        # 处理表单提交
        post.title = form.title.data
        post.content = form.content.data
        post.tags = form.tags.data
        post.summary = form.summary.data
        post.is_top = form.is_top.data
        post.archives = form.archives.data
        post.save()
        flash("博客更新成功", "success")
        return redirect(url_for("admin.blog_index"))
    return render_template("blog/editor.html", form=form, post=post)


@admin_bp.route("/blog/view/<int:post_id>")
def blog_view(post_id):
    """
    查看博客详情
    :param post_id: 博客ID
    :return: 渲染博客详情模板
    """
    post: Post = Post.get_or_none(Post.id == post_id)
    if not post:
        flash("博客不存在", "danger")
        return redirect(url_for("admin.blog_index"))
    # 渲染模板
    return render_template("blog/detail.html", post=post)


@admin_bp.route("/blog/delete/<int:post_id>")
@login_required
def blog_delete(post_id):
    """
    删除博客
    :param post_id: 博客ID
    :return: 重定向到博客主页
    """
    post: Post = Post.get_or_none(Post.id == post_id)
    if not post:
        flash("博客不存在", "danger")
        return redirect(url_for("admin.blog_index"))
    if post.cover:
        try:
            os.remove(os.path.join("app/static/blog/cover", post.cover))
        except FileNotFoundError:
            pass
    # 查找出博客内容中的所有图片
    soup = BeautifulSoup(post.content, "html.parser")
    img_srcs = [img["src"] for img in soup.find_all("img") if img.has_attr("src")]
    # 删除博客内容中的所有图片
    for img_src in img_srcs:
        img_path = os.path.join("app/static/blog/ck", img_src.split("/")[-1])
        try:
            os.remove(img_path)
        except FileNotFoundError:
            pass
    # 删除博客
    post.delete_instance()
    flash("博客删除成功", "success")
    return redirect(url_for("admin.blog_index"))


@admin_bp.route("/blog/cover/<int:post_id>", methods=["POST"])
@login_required
def blog_cover(post_id):
    """
    上传博客封面
    :param post_id: 博客ID
    :return: 重定向到博客主页
    """
    post: Post = Post.get_or_none(Post.id == post_id)
    if not post:
        flash("博客不存在", "danger")
        return redirect(url_for("admin.blog_index"))
    # 取出封面文件
    f = request.files.get("cover")
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
    filename = secure_filename(f.filename)
    # 检查是否存在旧封面
    if post.cover:
        # 删除旧封面
        try:
            os.remove(os.path.join("app/static/blog/cover", post.cover.split("/")[-1]))
        except FileNotFoundError:
            pass
    # 保存新封面
    f.save(os.path.join("app/static/blog/cover", filename))
    post.cover = "/static/blog/cover/" + filename
    post.save()
    # 返回成功消息
    flash(f"{post.title}封面上传成功", "success")
    return redirect(url_for("admin.blog_index"))


@admin_bp.route("/blog/archive")
@login_required
def blog_archive():
    """
    博客归档下载
    :return: 返回下载的归档文件
    """
    # 先打包一份最新的文件
    packaging_file("blog.tar.gz")
    return send_file(
        "blog.tar.gz",
        as_attachment=True,
        download_name="blog.tar.gz",
        mimetype="application/gzip",
    )


@admin_bp.route("/archive/index")
@login_required
def archive_index():
    """
    存档管理首页
    :return: 渲染存档管理首页模板
    """
    # 获取请求页
    page = request.args.get("page", 1, type=int)
    # 定义每一页显示的存档数量
    per_page = 12
    # 计算总页数
    total_pages = (Post.select().count() + per_page - 1) // per_page
    if page > total_pages:
        page = total_pages
    # 获取所有存档
    archives = (
        Archive.select().order_by(Archive.updated_at.desc()).paginate(page, per_page)
    )
    # 对每一个存档，获取关联的帖子
    for archive in archives:
        archive.posts = (
            Post.select()
            .where(Post.archives.contains(str(archive.id)))
            .order_by(Post.updated_at.desc())
        )  # 这里其实写得很屎，但是没关系，管理端慢点无所谓的
    # 前一页
    prev_page = page - 1 if page > 1 else None
    # 后一页
    next_page = page + 1 if page < total_pages else None
    # 渲染模板
    return render_template(
        "archive/index.html",
        archives=archives,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        current_page=page,
    )


@admin_bp.route("/archive/create", methods=["GET", "POST"])
@login_required
def archive_create():
    """
    创建存档
    :return: 渲染创建存档模板
    """
    form = ArchiveEditorForm()
    if form.validate_on_submit():
        # 处理表单提交
        archive = Archive.create(
            title=form.title.data,
            summary=form.summary.data,
        )
        if archive:
            flash("存档创建成功", "success")
        else:
            flash("存档创建失败", "danger")
        return redirect(url_for("admin.archive_index"))
    return render_template("archive/editor.html", form=form)


@admin_bp.route("/archive/edit/<int:archive_id>", methods=["GET", "POST"])
@login_required
def archive_edit(archive_id):
    """
    编辑存档
    :param archive_id: 存档ID
    :return: 渲染编辑存档模板
    """
    archive: Archive = Archive.get_or_none(Archive.id == archive_id)
    if not archive:
        flash("存档不存在", "danger")
        return redirect(url_for("admin.archive_index"))
    form = ArchiveEditorForm()
    if request.method == "GET":
        # 填充表单数据
        form.title.data = archive.title
        form.summary.data = archive.summary
    if form.validate_on_submit():
        # 处理表单提交
        archive.title = form.title.data
        archive.summary = form.summary.data
        archive.save()
        flash("存档更新成功", "success")
        return redirect(url_for("admin.archive_index"))
    return render_template("archive/editor.html", form=form, archive=archive)


@admin_bp.route("/archive/delete/<int:archive_id>")
@login_required
def archive_delete(archive_id):
    """
    删除存档
    :param archive_id: 存档ID
    :return: 重定向到存档管理首页
    """
    archive: Archive = Archive.get_or_none(Archive.id == archive_id)
    if not archive:
        flash("存档不存在", "danger")
        return redirect(url_for("admin.archive_index"))
    # 检查存档是否有关联的帖子
    posts = Post.select().where(Post.archives.contains(str(archive.id)))
    for post in posts:
        # 如果有关联的帖子，先删除关联
        temp_str = post.archives
        post.archives = ";".join(
            [x for x in temp_str.split(";") if x != str(archive.id)]
        )
        post.save()
    # 删除存档
    archive.delete_instance()
    flash("存档删除成功", "success")
    return redirect(url_for("admin.archive_index"))
