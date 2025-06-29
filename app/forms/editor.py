from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class BlogEditorForm(FlaskForm):
    """
    表单类，用于博客编辑器
    """

    title = StringField("标题", validators=[DataRequired()])
    summary = TextAreaField("摘要")
    content = CKEditorField("正文", validators=[DataRequired()])
    tags = StringField("标签（用;分开多个标签）")
    archives = StringField("存档（用;分开多个存档）")
    is_top = BooleanField("置顶", default=False)
    submit = SubmitField("提交")


class ArchiveEditorForm(FlaskForm):
    """
    表单类，用于存档编辑器
    """

    title = StringField("标题", validators=[DataRequired()])
    summary = TextAreaField("摘要")
    submit = SubmitField("提交")
