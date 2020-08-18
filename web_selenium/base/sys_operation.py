import os
import sys

'''
获取系统路径、生成文件路径、查找文件等功能
'''

current_path = os.path


def get_current_path() -> str:
    # 获取当前工作目录绝对路径
    return os.getcwd()


def get_all_subdirectories(path=get_current_path(), filter_name=None) -> list:
    # 获取目录下的文件名
    # 默认是当前目录
    # 根据filter_name指定所需文件，默认返回全部
    file = os.listdir(path)
    if filter_name:
        file = [file_name for file_name in file.copy() if filter_name in file_name]
    return file


def join_path(path, dir):
    return os.path.join(path, dir)


def get_env(key) -> str:
    # 获取环境变量
    return os.getenv(key)


if __name__ == '__main__':
    print(get_all_subdirectories(filter_name='py'))
    for file in get_all_subdirectories():
        print(join_path(get_current_path(), file))
