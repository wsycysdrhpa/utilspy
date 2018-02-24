#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/2/14'
# @description:


from math import sqrt

import numpy as np


class MathHelper(object):
    def __init__(self):
        pass

    # 求两列数值的对应元素乘积的总和
    @staticmethod
    def multi_col_2_sum(x, y):
        sum = 0.0
        for i in range(len(x)):
            sum += x[i] * y[i]
        return sum

    # 求两列数值的皮尔逊相关系数
    def cal_pearson_corr_coef(self, x, y):
        length = len(x)
        # 求和
        sum_1 = sum(x)
        sum_2 = sum(y)
        # 求乘积之和
        multiply_sum = self.multi_col_2_sum(x, y)
        # 求平方和
        x2_sum = sum([pow(i, 2) for i in x])
        y2_sum = sum([pow(j, 2) for j in y])
        num = multiply_sum - (float(sum_1) * sum_2 / length)
        # 计算皮尔逊相关系数
        den = sqrt((x2_sum - float(sum_1**2) / length) * (y2_sum - float(sum_2**2) / length))
        return num/den

    # 计算两个向量欧氏距离
    @staticmethod
    def cal_euclidean_dis(array_a, array_b):
        # array_a, array_b: numpy.array, 向量
        return np.sqrt((array_a - array_b).dot(array_a - array_b))

    @staticmethod
    def cal_cos_dis(array_a, array_b):
        # array_a, array_b: numpy.array, 向量
        return array_a.dot(array_b) / np.sqrt(array_a.dot(array_a) * array_b.dot(array_b))

    @staticmethod
    def sigmoid(x):
        return 1.0 / (1 + np.exp(-x))

    # 计算逆序数
    @staticmethod
    def cal_inverse_number(l1):
        cnt = 0
        for current_number in l1:
            for rear_number in l1[l1.index(current_number)+1:]:
                if current_number > rear_number:
                    cnt += 1
        return cnt


if __name__ == "__main__":
    pass
    math_helper = MathHelper()
    x = [1.0, 2.0, 3.0, 4.0]
    y = [40.0, 50.0, 70.0, 80.0]
    z = [50.0, 60.0, 70.0, 80.0]
    print math_helper.cal_pearson_corr_coef(x, y)
    print math_helper.cal_pearson_corr_coef(x, z)
    print math_helper.cal_pearson_corr_coef(y, z)

    a = [0, 1, 0, 3]
    b = [0, 1, 1, 1]

    print
    print math_helper.cal_pearson_corr_coef(a, b)  # 0.471404520791

    c = np.array([1, 1])
    d = np.array([2, 2])
    print
    print math_helper.cal_euclidean_dis(c, d)

    e =[4, 3, 2, 1]
    print
    print math_helper.cal_inverse_number(e)
