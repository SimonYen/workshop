import os
from typing import List


def get_files_in_filebin() -> List[str]:
    """
    获取文件存储目录下的所有文件名
    :return: 文件名列表
    """
    # 获取根目录
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filebin_path = os.path.join(root_path, "static", "filebin")
    if not os.path.exists(filebin_path):
        # 创建文件存储目录
        os.makedirs(filebin_path)
        return []

    files = []
    # 单层遍历文件存储目录
    for filename in os.listdir(filebin_path):
        files.append(filename)

    return files


def delete_file(file_path: str) -> bool:
    """
    删除指定路径的文件
    :param file_path: 文件的部分路径
    :return: 是否删除成功
    """
    # 获取根目录
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_path = os.path.join(root_path, "static")
    file_path = os.path.join(static_path, file_path)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False
