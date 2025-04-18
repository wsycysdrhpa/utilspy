import os
from os.path import dirname, join, exists


# 确定项目根目录
def find_project_root():
    current_file_path = os.path.abspath(__file__)
    """从当前路径向上查找，直到找到包含特定标识文件/目录的项目根目录"""
    # 可以根据项目特点添加其他标识文件，如 pyproject.toml, .git 等
    root_markers = ['.git', 'requirements.txt', 'setup.py', 'pyproject.toml']

    path = os.path.abspath(current_file_path)
    while path != os.path.dirname(path):  # 到达根目录时停止
        if any(exists(join(path, marker)) for marker in root_markers):
            return path
        path = os.path.dirname(path)

    # 如果没找到标识，则返回当前文件所在目录的上一级目录
    return dirname(dirname(current_file_path))


if __name__ == "__main__":
    print(find_project_root())
