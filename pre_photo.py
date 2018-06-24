# coding:utf-8

import cv2
import os


# 对图片进行二值化、边框检测和大小归一化



def bin_chinese(pathin, pathout):
    '''
    对图片进行二值化
    :return:
    '''
    pictures = os.listdir(pathin)
    for picture in pictures:
        pic_path = os.path.join(pathin, picture)
        # 以彩色图方式读取图片
        im = cv2.imread(pic_path)
        # 将图片转成灰度图
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        # 二值化
        retval, im_at_fixed = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY)
        # 保存图片
        pic_path = os.path.join(pathout, picture)
        cv2.imwrite(pic_path, im_at_fixed)

    print '二值化成功！'


def bor_chinese(pathin, pathout):
    '''
    对二值化后的图片进行边框提取
    :return:
    '''
    posup = 0
    posdown = 0
    posleft = 0
    posright = 0
    flag = 0

    pictures = os.listdir(pathin)
    for picture in pictures:
        pic_path = os.path.join(pathin, picture)
        # 以灰度图方式读取图片
        im = cv2.imread(pic_path, 0)
        width = len(im[0])
        height = len(im)
        # 找posup
        flag = 0
        for i in range(height):
            for j in range(width):
                if im[i][j] == 0:
                    posup = i
                    flag = 1
                    break
            if flag == 1:
                break

        # 找posdown
        flag = 0
        for i in range(height - 1, 0, -1):
            for j in range(width):
                if im[i][j] == 0:
                    posdown = i
                    flag = 1
                    break
            if flag == 1:
                break

        # 找posleft
        flag = 0
        for i in range(width):
            for j in range(height):
                if im[j][i] == 0:
                    posleft = i
                    flag = 1
                    break
            if flag == 1:
                break

        # 找posright
        flag = 0
        for i in range(width - 1, 0, -1):
            for j in range(height):
                if im[j][i] == 0:
                    posright = i
                    flag = 1
                    break
            if flag == 1:
                break

        # 裁剪图片
        im2 = im[posup:posdown, posleft:posright]

        # 保存图片
        pic_path = os.path.join(pathout, picture)
        cv2.imwrite(pic_path, im2)

    print '边框检测成功！'


def nor_chinese(pathin, pathout):
    '''
    对边框检测后的文字进行归一化
    :param pathin:
    :param pathout:
    :return:
    '''
    # 先调整文字比例
    # 高度填充
    pictures = os.listdir(pathin)
    for picture in pictures:
        pic_path = os.path.join(pathin, picture)
        # 以灰度图方式读取图片
        im = cv2.imread(pic_path, 0)
        width = len(im[0])
        height = len(im)
        h_ratio = width / height * 1.0
        w_ratio = height / width * 1.0

        # 高度填充
        if h_ratio > 1.25:
            Y = (width - height) / 2
            im = cv2.copyMakeBorder(im, Y, Y, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        # 宽度填充
        if w_ratio > 1.25:
            U = (height - width) / 2
            im = cv2.copyMakeBorder(im, 0, 0, U, U, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        # 采用双线性插值进行大小归一化
        im = cv2.resize(im, (64, 64))

        # 保存图片
        pic_path = os.path.join(pathout, picture)
        cv2.imwrite(pic_path, im)

    print '归一化成功！'


if __name__ == '__main__':
    # 二值化
    bin_chinese('./test', './test')
    # # 边框检测
    # bor_chinese('./bin_english', './bor_english')
    # # 归一化
    # nor_chinese('./bor_english', './nor_english')
    # # 最后二值化
    # bin_chinese('./nor_english', './res_english')
