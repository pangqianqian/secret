# -*- coding:utf-8 -*-  
# 生成的特征值直接写入当下文件夹的value.txt

import cv2 as cv
import os


def caculate_all(pathin):
    # 对64x64的字体进行特征提取
    pictures = os.listdir(pathin)
    for picture in pictures:
        HA = []  # 水平穿越的特征值
        VA = []  # 竖直穿越的特征值
        HA_H = []  # 水平半穿越的特征值
        VA_H = []  # 竖直半穿越的特征值
        cor_feature = []  # 四个角的能量值密度，左上，左下，右上，右下

        pic_path = os.path.join(pathin, picture)
        #  print pic_path
        im = cv.imread(pic_path, 0)
        # 水平全穿越
        HA.append(caculate_line(im[16]))
        HA.append(caculate_line(im[32]))
        HA.append(caculate_line(im[48]))

        # 竖直全穿越
        VA.append(caculate_line(im[16]))
        VA.append(caculate_line(im[32]))
        VA.append(caculate_line(im[48]))
        # 水平半穿越
        x = im[16]
        x1 = x[0:32]
        HA_H.append(caculate_line(x1))
        x2 = x[32:64]
        HA_H.append(caculate_line(x2))

        x = im[48]
        x1 = x[0:32]
        HA_H.append(caculate_line(x1))
        x2 = x[32:64]
        HA_H.append(caculate_line(x2))

        # 竖直半穿越
        y = [y[16] for y in im]  # 获取列

        y1 = y[0:32]
        VA_H.append(caculate_line(y1))
        y2 = y[32:64]
        VA_H.append(caculate_line(y2))

        y = [y[48] for y in im]

        y1 = y[0:32]
        VA_H.append(caculate_line(y1))
        y2 = y[32:64]
        VA_H.append(caculate_line(y2))

        # 测试打印特征值
        print pic_path
        print HA
        print VA
        print HA_H
        print VA_H
        #
        # 计算左上角的能量值
        cor_feature.append(cor_caculate(im, 0, 16, 0, 16))
        # 计算左下角的能量值
        cor_feature.append(cor_caculate(im, 48, 64, 0, 16))
        # 计算右上角的能量值
        cor_feature.append(cor_caculate(im, 0, 16, 48, 64))
        # 计算右下角的能量值
        cor_feature.append(cor_caculate(im, 48, 64, 48, 64))
        print cor_feature

        # 按格式写入文件
        name, ext = os.path.splitext(pic_path)
        name = os.path.basename(name)
        write_to_txt(name, HA, VA, HA_H, VA_H, cor_feature)


def caculate_line(line):
    # 计算该行或者列的特征值
    size = len(line)
    limit = 0  # 有无的界限
    k = 0  # 该行的特征值
    tag = 1
    for i in range(size):
        if line[i] == limit and tag == 1:
            k += 1
            tag = 0
        elif line[i] > limit:
            tag = 1
    return k


def cor_caculate(image, t_row, d_row, t_col, d_col):
    '''

    :param image: 输入图片
    :param t_row: 开始行
    :param d_row: 结束行
    :param t_col: 开始列
    :param d_col: 结束列
    :return: 能量值
    '''
    count = 0
    for i in range(t_row, d_row):
        for j in range(t_col, d_col):
            if image[i][j] == 0:  # 黑
                count += 1
    # print count * 1.0 / 256
    return count * 1.0 / 256


def write_to_txt(ch_name, HA, VA, HA_H, VA_H, cor_feature):
    try:
        fp = open("eng_value.txt", "a+")
        fp.write(ch_name)
        fp.write(",")

        for item in HA:
            fp.write(str(item) + " ")
        fp.write(",")

        for item in VA:
            fp.write(str(item) + " ")
        fp.write(",")

        for item in HA_H:
            fp.write(str(item) + " ")
        fp.write(",")

        for item in VA_H:
            fp.write(str(item) + " ")
        fp.write(",")

        for item in cor_feature:
            fp.write(str(item) + " ")

        fp.write("\n")
        fp.close()

    except IOError:
        print("fail to open value.txt")


if __name__ == '__main__':
    caculate_all('./res_english')
