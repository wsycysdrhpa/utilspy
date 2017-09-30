# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '14-4-12'


import os
import shutil
import zipfile


class ZipHelper():
    def __init__(self):
        pass

    def zip_file(self, file_name, zip_file_name, is_delete=False):
        zip_file = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        zip_file.write(file_name)
        zip_file.close()
        if is_delete:
            os.remove(file_name)

    def unzip(self, zip_file_path, out_dir="", is_save_path=True):
        """
        解压zip文件
        @param zip_file_path:压缩包路径
        @param out_dir:输出目录,默认为""即当前工作目录下
        @param is_save_path:是否保留压缩包内部路径，默认保留。
                            True：保留，False：不保留，即把压缩包内所有文件解压到out_dir目录下
        """
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        zip_file = zipfile.ZipFile(zip_file_path, 'r')
        for file_name in zip_file.namelist():
            source = zip_file.open(file_name)
            if is_save_path:
                file_name = os.path.join(out_dir, file_name)
                dir_name = os.path.dirname(file_name)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
            else:
                file_name = os.path.join(out_dir, os.path.basename(file_name))
            if os.path.isdir(file_name):
                continue
            target = file(file_name, "wb")
            shutil.copyfileobj(source, target)
            source.close()
            target.close()
        zip_file.close()

    def zip_dir(self, dir_name, zip_file_name, is_delete=False):
        """
        压缩文件夹到指定文件中
        @param dir_name:文件夹路径
        @param zip_file_name:压缩后文件路径
        @param is_delete: 是否删除源文件
        """
        file_list = []
        if os.path.isfile(dir_name):
            file_list.append(dir_name)
        else:
            for root, dirs, files in os.walk(dir_name):
                for name in files:
                    file_list.append(os.path.join(root, name))
        zip_file = zipfile.ZipFile(zip_file_name, "w", zipfile.zlib.DEFLATED)
        for file_path in file_list:
            zip_file.write(file_path)
            if is_delete:
                os.remove(file_path)
        zip_file.close()

    def unzip_(self, zip_file_path, out_dir="", is_save_path=True):
        """
        解压zip文件
        @param zip_file_path:压缩包路径
        @param out_dir:输出目录,默认为""即当前工作目录下
        @param is_save_path:是否保留压缩包内部路径，默认保留。
                            True：保留，False：不保留，即把压缩包内所有文件解压到out_dir目录下
        """
        zip_file = zipfile.ZipFile(zip_file_path, 'r')
        for file_name in zip_file.namelist():
            # 用read可能会超内存，改用unzip方法，用shutil.copyfileobj
            data = zip_file.read(file_name)
            if is_save_path:
                file_name = os.path.join(out_dir, file_name)
                dir_name = os.path.dirname(file_name)
                if not os.path.exists(dir_name):
                    os.mkdir(dir_name)
            else:
                file_name = os.path.join(out_dir, os.path.basename(file_name))
            with open(file_name, "w+b") as out_file:
                out_file.write(data)
        zip_file.close()

    def unzip__(self, zip_file_path, out_dir="", is_save_path=True):
        zip_file = zipfile.ZipFile(zip_file_path, 'r')
        for file_name in zip_file.namelist():
            zip_file.extract(file_name, out_dir)
        zip_file.close()


if __name__ == "__main__":
    pass
