from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user
from app.forms.editor import BlogEditorForm
from app.models.post import Post

admin_bp = Blueprint("admin", __name__)


@login_required
@admin_bp.route("/admin/blog/index")
def blog_index():
    """
    博客管理首页
    :return: 渲染博客管理首页模板
    """
    # 获取所有博客
    posts = Post.select().order_by(Post.updated_at.desc())
    return render_template("blog/index.html", posts=posts)


@login_required
@admin_bp.route("/admin/blog/create", methods=["GET", "POST"])
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
