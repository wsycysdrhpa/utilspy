# -*- coding:utf-8 -*-


# @version: 1.0
# @author: daichi
# @date: '14-8-8'


import os
import re
from utilspy.list.list_util import list_duplicate_removal


def delete_file_folder(src):
    #  delete files
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    # if data is dir just delete the child data and dir ,keep the current dir
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            delete_file_folder(itemsrc)

def get_file_path_under_dir(path, filter_regex=None):
    current_files = os.listdir(path)
    all_files = []
    for file_name in current_files:
        full_file_name = os.path.join(path, file_name)
        if os.path.isdir(full_file_name):
            next_level_files = get_file_path_under_dir(full_file_name)
            all_files.extend(next_level_files)
        else:
            if filter_regex:
                if re.search(filter_regex,full_file_name):
                    all_files.append(full_file_name)
            else:
                all_files.append(full_file_name)
    return all_files

def load_data_from_file(file_name):
    return_list = []
    file = open(file_name, 'r')
    lines = file.readlines()
    for line in lines:
        return_list.append(line.strip())
    file.close()
    return return_list


def load_data_from_file_paths(files):
    return_list = []
    for file_path in files:
        return_list+=load_data_from_file(file_path)
    return return_list


def extractor_one_word_in_file(file_path,extractor_file_name, encode):
    file = open(file_path,'r')
    extractor_file = open(extractor_file_name,'a')
    lines = file.readlines()
    for line in lines:
        if re.search(u'^[\u4E00-\u9FA5]$', line.strip().decode(encode)) is not None:
            extractor_file.write(line.strip() + '\n')
            print(line)
        if len(str(line.strip())) == 1:
            extractor_file.write(line.strip() + '\n')
            print(line)
    file.close()
    extractor_file.close()


def file_duplicate_removal_merger(file_path1, file_path2, merge_file_name):
    file1 = open(file_path1, 'r')
    file2 = open(file_path2, 'r')
    merge_file = open(merge_file_name, 'a')
    data = file1.readlines() + file2.readlines()
    data = list_duplicate_removal(data)
    for line in data:
        merge_file.write(line.strip() + '\n')
        print(line)
    file1.close()
    file2.close()
    merge_file.close()

def merge_files(file_path_list, merge_file_path, duplicate_removal=False):
    line_list = []
    merge_file = open(merge_file_path,'a')
    for file_path in file_path_list:
        with open(file_path,'r') as file:
            for line in file:
                if len(line_list) > 5000:
                    if duplicate_removal:
                        merge_file.write(''.join(list(set(line_list))))
                    else:
                        merge_file.write(''.join(line_list))
                    line_list = []
                    merge_file.flush()
                line_list.append(line)
    if line_list:
        if duplicate_removal:
            merge_file.write(''.join(list(set(line_list))))
        else:
            merge_file.write(''.join(line_list))
        merge_file.flush()
    merge_file.close()

def split_file(file_name, count):
    file = open(file_name, 'r')
    lines = file.readlines()
    size = int(len(lines)/count)
    for index in range(0, count):
        sub_file = open(file_name+str(index+1)+'.sub','a')
        if index == (count-1):
            sub_file.writelines(lines[(index)*size:])
        else:
            sub_file.writelines(lines[(index)*size:(index+1)*size])
        sub_file.flush()
        sub_file.close()
    file.close()
    print('split ok!')


if __name__=='__main__':
    pass
