#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2021/5/10'
# @description:


import codecs


from utilspy.excel.excel_read_helper import ExcelReadHelper
from utilspy.excel.excel_write_helper import ExcelWriteHelper


class ExcelHelper(object):
    def __init__(self):
        self.excel_read_helper = ExcelReadHelper()
        self.excel_write_helper = ExcelWriteHelper()

    # excel头不做区分
    def excel2txt(self, excel_path, txt_path, sheet_col):
        """
        
        :param excel_path: excel路径 
        :param txt_path: txt路径
        :param sheet_col: 表序号，从0开始
        :return: 
        """
        ws = self.excel_read_helper.read_from_excel(excel_path, sheet_col)
        with codecs.open(txt_path, "wb", 'utf-8') as txt_fp:
            for r in range(ws.nrows):
                rows = ws.row_values(r)
                rows = [str(r) for r in rows]
                # print(rows)
                txt_fp.write("\t".join(rows) + "\n")

    # excel头不做区分
    def txt2excel(self, txt_path, excel_path, sheet_name):
        """
        
        :param txt_path: txt路径
        :param excel_path: excel路径 
        :param sheet_name: excel表名
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
        self.excel_write_helper.write_to_excel(excel_path, sheet_name, rows)


if __name__ == "__main__":
    pass
    excel_helper = ExcelHelper()
    excel_helper.excel2txt(r"./data/example.xls", r"./data/example.txt", 0)
    excel_helper.txt2excel(r"./data/example.txt", r"./data/example2.xls", "test")
