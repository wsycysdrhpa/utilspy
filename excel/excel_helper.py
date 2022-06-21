#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2021/5/10'
# @description:


import codecs
import re


from utilspy.excel.excel_read_helper import ExcelReadHelper
from utilspy.excel.excel_write_helper import ExcelWriteHelper


class ExcelHelper(object):
    def __init__(self):
        self.re_noise = re.compile("[\t\r\n]")
        self.excel_read_helper = ExcelReadHelper()
        self.excel_write_helper = ExcelWriteHelper()

    def excel2txt(self, excel_path, txt_path, sheet_col, is_contain_header=True):
        """
        
        :param excel_path: excel路径, 支持xls和xlsx格式
        :param txt_path: txt路径
        :param sheet_col: 表序号，从0开始
        :param is_contain_header: 是否需要包含头，是的话包含第一行，否则不包含
        :return: 
        """
        ws = self.excel_read_helper.read_from_excel(excel_path, sheet_col)
        with codecs.open(txt_path, "wb", 'utf-8') as txt_fp:
            for i in range(ws.nrows):
                rows = ws.row_values(i)
                for j in range(len(rows)):
                    rows[j] = str(rows[j])
                    rows[j] = self.re_noise.sub("  ", rows[j])
                # print(rows)
                if not is_contain_header and i==0:
                    continue
                txt_fp.write("\t".join(rows) + "\n")

    def txt2excel(self, txt_path, excel_path, sheet_name, header=()):
        """
        
        :param txt_path: txt路径
        :param excel_path: excel路径, 支持xls格式，不支持xlsx格式
        :param sheet_name: excel表名
        :param header: just like ["id", "name", "age"] or ("id", "name", "age")
        :return: 
        """
        rows = []
        with codecs.open(txt_path, "rb", "utf-8", errors="ignore") as txt_fp:
            for line in txt_fp:
                line_lst = []
                line = line.strip()
                # print(line)
                for e in line.split("\t"):
                    line_lst.append(e)
                # print(line_lst)
                rows.append(line_lst)
            # print(rows)
        if not header:
            self.excel_write_helper.write_to_excel(excel_path, sheet_name, rows)
        else:
            self.excel_write_helper.write_to_excel_with_head(excel_path, sheet_name, header, rows)


if __name__ == "__main__":
    pass
    excel_helper = ExcelHelper()
    excel_helper.excel2txt(r"./data/example_with_header.xls", r"./data/example_with_header.txt", 0, is_contain_header=True)
    excel_helper.excel2txt(r"./data/example_with_header.xls", r"./data/example.txt", 0, is_contain_header=False)

    excel_helper.txt2excel(r"./data/example.txt", r"./data/example2.xls", "test", [])
    excel_helper.txt2excel(r"./data/example.txt", r"./data/example2_with_header.xls", "test", ("id", "name", "age"))
