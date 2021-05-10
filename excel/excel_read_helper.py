#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2021/5/8'
# @description: Reference: https://github.com/jumper2014/PyCodeComplete: 68


import xlrd


class ExcelReadHelper(object):
    def __init__(self):
        pass

    def read_from_excel(self, workbook_path, sheet_col):
        wb = xlrd.open_workbook(workbook_path)
        ws = wb.sheet_by_index(sheet_col)
        return ws


if __name__ == "__main__":
    pass
    excel_read_helper = ExcelReadHelper()
    ws = excel_read_helper.read_from_excel(r'./data/example.xls', sheet_col=0)

    # 获取每行数据，处理数据时需要注意第一行是否是表头
    for r in range(ws.nrows):
        rows = ws.row_values(r)
        print(rows)
