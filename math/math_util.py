# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '2016/12/29'


import numpy


def euclidean_distance(array_a, array_b):
    # array_a, array_b: numpy.array, 向量
    return numpy.sqrt((array_a-array_b).dot(array_a-array_b))

def cos(array_a, array_b):
    # array_a, array_b: numpy.array, 向量
    return array_a.dot(array_b)/numpy.sqrt(array_a.dot(array_a)*array_b.dot(array_b))

def sigmoid(x):
    return 1.0/(1+numpy.exp(-x))


if __name__ == "__main__":
    pass