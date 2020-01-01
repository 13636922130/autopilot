import numpy as np
from scipy.optimize import leastsq


def __func(self, p, x):
    '''
    最小二乘法拟合直线
    需要拟合的函数func :指定函数的形状
    '''
    k, b = p
    return k * x + b


def __error(self, p, x, y):
    '''
    偏差函数：x,y都是列表:这里的x,y更上面的Xi,Yi中是一一对应的
    '''
    return self.__func(p, x) - y


def LSM_test(lines):
    '''
    最小二乘法拟合
        对直线参数用最小二乘法进行拟合，得到左右车道两条线条的斜率和截距
    参数：
        lines: 车道识别后的直线参数
    返回值：
        k1, b1, k2, b2: 两条线条的斜率和截距
    '''
    left_flag = False  # 标志位初始化为False
    right_flag = False

    left_line = np.empty([2, 0])  # 存放左边车道的数据
    right_line = np.empty([2, 0])  # 存放右边车道的数据

    for x1, y1, x2, y2 in lines:
        # 依据斜率分为左右车道
        # 左边车道
        if (x1 - x2 < 0 and y1 - y2 < 0) or (x2 - x1 < 0 and y2 - y1 < 0):
            __leftFlag = True
            left_line = np.append(left_line, [[x1, x2], [y1, y2]], axis=1)
        # 右边车道
        else:
            __rightFlag = True
            right_line = np.append(right_line, [[x1, x2], [y1, y2]], axis=1)

    # k,b的初始值，可以任意设定,经过几次试验，发现p的值会影响cost的值：Para[1]
    p = [1, 20]

    # 把error函数中除了p0以外的参数打包到args中(使用要求)
    if __leftFlag:
        Para1 = leastsq(__error, p, args=(left_line[0, :], left_line[1, :]))
    if __rightFlag:
        Para2 = leastsq(__error, p, args=(right_line[0, :], right_line[1, :]))

    # 识别后的两条直线的斜率和截距
    k1 = b1 = k2 = b2 = 0
    if __leftFlag:
        k1, b1 = Para1[0]
    if __rightFlag:
        k2, b2 = Para2[0]
    return k1, b1, k2, b2

lines = np.array([[  0, 30,319, 30],
 [117, 88,159, 91],
 [241,159,244, 77],
 [ 71, 53,138, 69],
 [ 92,151,111,151],
 [ 47,142, 73,142],
 [136,150,187,150],
 [159,153,235,157]
 ])
k1, b1, k2, b2 = LSM_test(lines)