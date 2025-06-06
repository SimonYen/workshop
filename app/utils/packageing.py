import os
import tarfile

# 获取项目根目录
def get_project_root() -> str:
    """
    获取项目根目录
    :return: 项目根目录路径
    """
    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.dirname(app_path)

# 打包文件
def packaging_file(archive_name: str)->None:
    """
    打包文件
    :param archive_name: 打包后的文件名
    :return: None
    """
    root_path = get_project_root()
    archive_path = os.path.join(root_path, "app", archive_name)
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(os.path.join(root_path, "app","static","blog"), arcname="blog")
        tar.add(os.path.join(root_path,"workshop.db"),arcname="workshop.db")

if __name__ == "__main__":
    # 测试获取项目根目录
    print(get_project_root())
    packaging_file("test.tar.gz")