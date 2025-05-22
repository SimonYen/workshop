import os
import tomllib

class Config:
    """基础配置类"""
    DEBUG = False
    
    def __init__(self):
        # 加载配置文件
        self.data = tomllib.load(open('app.toml', 'rb'))
        # 将配置项设置为类属性而不是实例属性
        Config.SECRET_KEY = self.data['default']['SECRET_KEY']
        Config.DB_URL=self.data['default']['DB_URL']


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
    def __init__(self):
        super().__init__()
        # 将配置项设置为类属性
        data = self.data['development']
        DevelopmentConfig.HOST = data['HOST']
        DevelopmentConfig.PORT = data['PORT']


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    PORT = os.environ.get('SERVER_PORT', 5000)

# 配置映射
config = {
    'development': DevelopmentConfig(),
    'production': ProductionConfig(),
    'default': DevelopmentConfig()
}