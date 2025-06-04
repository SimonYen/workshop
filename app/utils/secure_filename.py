import uuid
import os


def secure_filename(filename: str) -> str:    
    """
    生成安全的文件名，避免文件名中包含特殊字符或路径穿越攻击。
    :param filename: 原始文件名
    :return: GUID文件名
    """
    # 生成一个唯一的GUID
    guid = str(uuid.uuid4())
    # 获取文件扩展名
    _, ext = os.path.splitext(filename)
    # 返回安全的文件名
    return f"{guid}{ext.lower()}" if ext else guid