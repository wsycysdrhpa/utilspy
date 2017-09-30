#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @version: 1.0
# @author: Aruan
# @email: Arain2011@foxmail.com
# @update: '2016/12/8'
# @description:


from math import sqrt


class MathUtil(object):
    def __init__(self):
        pass

    # 求两列数值的对应元素乘积的总和
    def multiply(self, x, y):
        multiply_sum = 0.0
        for i in range(len(x)):
            multiply_sum += x[i]*y[i]
        return multiply_sum

    # 求两列数值的皮尔逊相关系数
    def cal_corr_coef(self, x, y):
        length = len(x)
        # 求和
        sum_1 = sum(x)
        sum_2 = sum(y)
        # 求乘积之和
        multiply_sum = self.multiply(x, y)
        # 求平方和
        x2_sum = sum([pow(i, 2) for i in x])
        y2_sum = sum([pow(j, 2) for j in y])
        num = multiply_sum - (float(sum_1)*sum_2/length)
        # 计算皮尔逊相关系数
        den = sqrt((x2_sum-float(sum_1**2)/length)*(y2_sum-float(sum_2**2)/length))
        return num/den


if __name__ == "__main__":
    pass
    math_util = MathUtil()
    x = [1.0, 2.0, 3.0, 4.0]
    y = [40.0, 50.0, 70.0, 80.0]
    z = [50.0, 60.0, 70.0, 80.0]
    print math_util.cal_corr_coef(x,y)
    print math_util.cal_corr_coef(x,z)
    print math_util.cal_corr_coef(y,z)

    a = [0, 1, 0, 3]
    b = [0, 1, 1, 1]

    print math_util.cal_corr_coef(a,b)  # 0.471404520791