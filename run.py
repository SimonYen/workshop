from app import create_app
import os

# 从环境变量获取配置名称，默认为 'default'
config_name = os.getenv("FLASK_CONFIG", "default")

# 创建 Flask 应用实例
app = create_app(config_name)

if __name__ == "__main__":
    # 获取静态文件根目录
    static_root = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "app", "static"
    )
    # filebin目录
    filebin_dir = os.path.join(static_root, "filebin")
    # blog目录
    blog_dir = os.path.join(static_root, "blog")
    # blog/cover目录
    blog_cover_dir = os.path.join(blog_dir, "cover")
    # blog/ckeditor目录
    blog_ckeditor_dir = os.path.join(blog_dir, "ck")
    # 检查并创建必要的目录
    os.makedirs(filebin_dir, exist_ok=True)
    os.makedirs(blog_dir, exist_ok=True)
    os.makedirs(blog_cover_dir, exist_ok=True)
    os.makedirs(blog_ckeditor_dir, exist_ok=True)
    # 启动应用
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=False)
