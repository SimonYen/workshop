from app import create_app
import os

# 从环境变量获取配置名称，默认为 'default'
config_name = os.getenv("FLASK_CONFIG", "default")

# 创建 Flask 应用实例
app = create_app(config_name)

if __name__ == "__main__":
    # 启动应用
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=False)
