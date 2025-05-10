import os

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 9999



class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    HOST= os.environ.get('SERVER_HOST', '0.0.0.0')
    PORT= os.environ.get('SERVER_PORT', 5000)


# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}