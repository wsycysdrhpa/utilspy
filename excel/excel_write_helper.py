#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2021/5/8'
# @description: Reference: https://github.com/jumper2014/PyCodeComplete: 69


import xlwt


class ExcelWriteHelper(object):
    def __init__(self):
        pass

    def write_to_excel(self, workbook_name, sheet_name, rows):
        """
        
        :param workbook_name: 
        :param sheet_name: 
        :param rows: 
        :return: 
        """
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(sheetname=sheet_name)

        # 逐行写入
        row_num = 0
        for row in rows:
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num])
            row_num += 1

        wb.save(filename_or_stream=workbook_name)

    def write_to_excel_with_head(self, workbook_name, sheet_name, header, rows):
        """
        
        :param workbook_name: 
        :param sheet_name: 
        :param header: 
        :param rows: 
        :return: 
        """
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(sheetname=sheet_name)

        # 写入表头
        for col_num in range(len(header)):
            ws.write(0, col_num, header[col_num])

        # 逐行写入
        row_num = 1
        for row in rows:
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num])
            row_num += 1

        wb.save(filename_or_stream=workbook_name)


if __name__ == "__main__":
    pass
    excel_write_helper = ExcelWriteHelper()
    header = ["id", "name", "age"]
    # 行数据
    rows = [
        [1, 'Python', 30],
        [2, 'Perl', 33],
        [3, 'Ruby', 20]
    ]

    excel_write_helper.write_to_excel_with_head(r"./data/example_with_head.xls", 'My Sheet', header, rows)

    excel_write_helper.write_to_excel(r"./data/example.xls", 'My Sheet', rows)
