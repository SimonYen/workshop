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
