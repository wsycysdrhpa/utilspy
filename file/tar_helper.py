# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '14-4-12'


import os
import tarfile


class TarHelper():
    def __init__(self):
        pass

    def tar_file(self, file_name, tar_file_name, mode="w:gz"):
        tar = tarfile.open(tar_file_name, mode)
        tar.add(file_name)
        tar.close()

    def tar_dir(self, dir_name, tar_file_name, mode="w:gz"):
        file_list = []
        if os.path.isfile(dir_name):
            file_list.append(dir_name)
        else:
            for root, dirs, files in os.walk(dir_name):
                for name in files:
                    file_list.append(os.path.join(root, name))
        tar = tarfile.open(tar_file_name, mode)
        for file_path in file_list:
            tar.add(file_path)
        tar.close()

    def untar_file(self, tar_file_name, file_name, mode="r:gz"):
        tar = tarfile.open(tar_file_name, mode)
        #path为文件夹名
        tar.extractall(path=file_name)
        tar.close()


if __name__ == "__main__":
    helper = TarHelper()
    #helper.tar_file("result_6.txt", "result_6.tar.gz")
    helper.untar_file("result_6.tar.gz", "upload")
    pass
