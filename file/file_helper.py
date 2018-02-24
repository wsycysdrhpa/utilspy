# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '14-4-16'


import os
import shutil


class FileHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def get_file_list(dir_name):
        file_list = []
        for root, dirs, files in os.walk(dir_name):
            for file_name in files:
                file_list.append(os.path.join(root, file_name))
        return file_list

    @staticmethod
    def rename(old_file_name, new_file_name):
        os.rename(old_file_name, new_file_name)

    @staticmethod
    def get_file_size(file_path):
        """
        获取文件大小，单位字节(B)
        @param file_path:
        @return:
        """
        return os.path.getsize(file_path)

    @staticmethod
    def make_dir(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def get_dir_size(dir_name):
        size = 0L
        for root, dirs, files in os.walk(dir_name):
            for file_name in files:
                size += FileHelper.get_file_size(os.path.join(root, file_name))
        return size

    @staticmethod
    def remove_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def remove_dir(dir_path, is_remove_dir=True):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            if not is_remove_dir:
                FileHelper.make_dir(dir_path)

    @staticmethod
    def move_file(path, new_path):
        shutil.move(path, new_path)

    @staticmethod
    def copy_file(src_file, des_file):
        shutil.copy(src_file, des_file)

    @staticmethod
    def copy_dir(src_dir, des_dir):
        FileHelper.remove_dir(des_dir)
        shutil.copytree(src_dir, des_dir)

    @staticmethod
    def copy_sub_files(src_dir, des_dir):
        # cp -R src_dir/* des_dir/
        for path in os.listdir(src_dir):
            src = os.path.join(src_dir, path)
            des = os.path.join(des_dir, path)
            if os.path.isdir(src):
                FileHelper.copy_dir(src, des)
            else:
                FileHelper.copy_file(src, des)

    @staticmethod
    def remove_sub_files(src_dir):
        # rm -r src_dir/*
        for path in os.listdir(src_dir):
            src = os.path.join(src_dir, path)
            if os.path.isdir(src):
                FileHelper.remove_dir(src)
            else:
                FileHelper.remove_file(src)


if __name__ == "__main__":
    pass
