__auther__ = 'chenyiqun'

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

class RoadRecognition(object):

    def __init__(self):
        self.filterSize = 7 #滤波核大小
        self.cannyMin = 50 #Canny边缘提取设置最小值
        self.cannyMax = 255 #Canny边缘提取设置最大值
        self.__leftFlag = False #是否识别到左侧车道
        self.__rightFlag = False #是否识别到右侧车道

    def __func(self, p, x):
        '''
        最小二乘法拟合直线
        需要拟合的函数func :指定函数的形状
        '''
        k, b = p
        return k*x+b

    def __error(self, p, x, y):
        '''
        偏差函数：x,y都是列表:这里的x,y更上面的Xi,Yi中是一一对应的
        '''
        return self.__func(p, x) - y

    def imageProcess(self, img):
        '''
        对图像数据进行处理
            对图像进行裁剪、翻转、灰度化、中值模糊、Canny边缘检测后
            再进行霍夫变换检测直线,得到直线参数
        参数：
            img: 车道图像
        返回值：
            lines: 车道识别后的直线参数
                   是一个nx4的矩阵,每有一行代表一条直线参数
                   每一列都有直线的起始点坐标x1, y1, 终点坐标x2, y2
                   如果没有识别到车道返回None
        '''
        cropImg = img[80:] #图片裁剪

        grayImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY) #灰度化
        medianImg = cv2.medianBlur(grayImg, self.filterSize) #中值模糊
        cannyMedianImg = cv2.Canny(medianImg, self.cannyMin, self.cannyMax)  #Canny边缘检测

        lines = cv2.HoughLinesP(cannyMedianImg, 1, np.pi / 180, 30, minLineLength=5, maxLineGap=10)  #霍夫变换道路检测
        if lines is None: #没有识别到车道的情况
            return None
        else:
            return lines[:, 0, :]

    def LSM(self, lines):
        '''
        最小二乘法拟合
            对直线参数用最小二乘法进行拟合，得到左右车道两条线条的斜率和截距
        参数：
            lines: 车道识别后的直线参数
        返回值：
            k1, b1, k2, b2: 两条线条的斜率和截距
        '''
        self.__leftFlag = False #标志位初始化为False
        self.__rightFlag = False

        left_line = np.empty([2, 0])  # 存放左边车道的数据
        right_line = np.empty([2, 0])  # 存放右边车道的数据

        for x1, y1, x2, y2 in lines:
            # 依据斜率分为左右车道
            # 左边车道
            if (x1 - x2 < 0 and y1 - y2 < 0) or (x2 - x1 < 0 and y2 - y1 < 0):
                self.__leftFlag = True
                left_line = np.append(left_line, [[x1, x2], [y1, y2]], axis=1)
            # 右边车道
            else:
                self.__rightFlag = True
                right_line = np.append(right_line, [[x1, x2], [y1, y2]], axis=1)

        #print('left-line shape:', left_line.shape)
        #print('right-line shape:', right_line.shape)

        # k,b的初始值，可以任意设定,经过几次试验，发现p的值会影响cost的值：Para[1]
        p = [1, 20]

        # 把error函数中除了p0以外的参数打包到args中(使用要求)
        if self.__leftFlag:
            Para1 = leastsq(self.__error, p, args=(left_line[0, :], left_line[1, :]))
        if self.__rightFlag:
            Para2 = leastsq(self.__error, p, args=(right_line[0, :], right_line[1, :]))

        #识别后的两条直线的斜率和截距
        k1 = b1 = k2 = b2 = 0
        if self.__leftFlag:
            k1, b1 = Para1[0]
        if self.__rightFlag:
            k2, b2 = Para2[0]
        return k1, b1, k2, b2

    def turnPredition(self, k1, b1, k2, b2):
        '''
        转向预测
            通过拟合后的两条直线判断是否需要转向
        参数：
            img: 车道图像
        '''
        print(k1, b1, k2, b2)

    def recognize(self, img):
        '''
        车道识别
            调用imageProcess、LSM、turnPredition三个函数
            最终实现对车道的识别并控制转向
        参数：
            img: 车道图像
        '''
        lines = self.imageProcess(img)
        if lines is None:
            print('Without road!')
        else:
            k1, b1, k2, b2 = self.LSM(lines)
            self.turnPredition(k1, b1, k2, b2)

    def visualize(self):
        '''
        可视化
            对实时车道识别的可视化
        '''
        cap = cv2.VideoCapture(0)  # 获取摄像头
        cap.set(3, 320)  # 设置分辨率为320x240
        cap.set(4, 240)

        while True:
            ret, img = cap.read()  # 获取当前视频帧
            lines = self.imageProcess(img)  #图像处理

            if lines is None:  # 如果检测不到车道
                continue  # 获取下一帧视频
            else:
                k1, b1, k2, b2 = self.LSM(lines)  # 最小二乘法拟合
                if k1 != 0 or b1 != 0:
                    b1 += 80
                    cv2.line(img, (0, int(b1)), (320, int(k1 * 320 + b1)), (255, 0, 0), 2)

                if k2 != 0 or b2 != 0:
                    b2 += 80
                    cv2.line(img, (0, int(b2)), (320, int(k2 * 320 + b2)), (0, 0, 255), 2)

            cv2.imshow('Visualization', img)  # 显示视频帧

            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q退出
                break
 
        cap.release()
        cv2.destroyAllWindows()

    def testOneImage(self, img):
        '''
        对一张图像进行车道识别,并对结果进行可视化
        参数：
            img: 图像数据
        '''

        cropImg = img[80:]  # 图片裁剪
        grayImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)  # 灰度化
        medianImg = cv2.medianBlur(grayImg, self.filterSize)  # 中值模糊
        cannyMedianImg = cv2.Canny(medianImg, self.cannyMin, self.cannyMax)  # Canny边缘检测
        cv2.imshow('Canny', cannyMedianImg)


        lines = self.imageProcess(img) #图像处理

        if lines is not None:  # 如果检测到车道
            k1, b1, k2, b2 = self.LSM(lines)  # 最小二乘法拟合
            if k1 != 0 or b1 != 0:
                b1 += 80
                cv2.line(img, (0, int(b1)), (320, int(k1 * 320 + b1)), (255, 0, 0), 2)

            if k2 != 0 or b2 != 0:
                b2 += 80
                cv2.line(img, (0, int(b2)), (320, int(k2 * 320 + b2)), (0, 0, 255), 2)

        cv2.imshow('TestOneImage', img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
