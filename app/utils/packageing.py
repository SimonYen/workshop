import os

# 获取项目根目录
def get_project_root() -> str:
    """
    获取项目根目录
    :return: 项目根目录路径
    """
    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.dirname(app_path)


if __name__ == "__main__":
    # 测试获取项目根目录
    print(get_project_root())