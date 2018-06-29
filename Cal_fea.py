# -*- coding:utf-8 -*-  
'''
功能：求文字图片图片,并写入value.txt
'''

import cv2 as cv
import os


class Calfea:
    def __init__(self):
        self.calpath = "./result/"

    def caculate_all(self, fpath, ffpath, pathin):
        # 对64x64的字体进行特征提取
        pictures = os.listdir(pathin)
        for picture in pictures:
            pic_path = os.path.join(pathin, picture)
            feature = self.caculate(pic_path)
            HA = feature[0]
            VA = feature[1]
            HA_H = feature[2]
            VA_H = feature[3]
            cor_feature = feature[4]
            # 按格式写入文件
            # name, ext = os.path.splitext(pic_path)
            # name = os.path.basename(name)
            name = fpath + ffpath + os.path.splitext(picture)[0]
            name = pic_path
            self.write_to_txt(name, HA, VA, HA_H, VA_H, cor_feature)

    def caculate(self, im_path):
        HA = []  # 水平穿越的特征值
        VA = []  # 竖直穿越的特征值
        HA_H = []  # 水平半穿越的特征值
        VA_H = []  # 竖直半穿越的特征值
        cor_feature = []  # 四个角的能量值密度，左上，左下，右上，右下

        im = cv.imread(im_path, 0)
        '''
        三行取最大值
        '''
        # 水平全穿越
        xlist1 = im[14:17]
        HA.append(self.caculate_three_lines(xlist1))
        xlist2 = im[30:33]
        HA.append(self.caculate_three_lines(xlist2))
        xlist3 = im[46:49]
        HA.append(self.caculate_three_lines(xlist3))

        # 竖直全穿越
        y1 = [y[14] for y in im]  # 获取三列
        y2 = [y[15] for y in im]
        y3 = [y[16] for y in im]
        ylist1 = [y1, y2, y3]
        VA.append(self.caculate_three_lines(ylist1))

        y1 = [y[30] for y in im]  # 获取三列
        y2 = [y[31] for y in im]
        y3 = [y[32] for y in im]
        ylist2 = [y1, y2, y3]
        VA.append(self.caculate_three_lines(ylist2))

        y1 = [y[46] for y in im]  # 获取三列
        y2 = [y[47] for y in im]
        y3 = [y[48] for y in im]
        ylist3 = [y1, y2, y3]
        VA.append(self.caculate_three_lines(ylist3))

        '''水平半穿越'''
        # 上三行像素
        x1 = im[14]
        x2 = im[15]
        x3 = im[16]
        # 左上
        x_half_list1 = [x1[0:32], x2[0:32], x3[0:32]]

        HA_H.append(self.caculate_three_lines(x_half_list1))
        # 右上
        x_half_list2 = [x1[32:64], x2[32:64], x3[32:64]]
        HA_H.append(self.caculate_three_lines(x_half_list2))

        # 下三行像素
        x1 = im[46]
        x2 = im[47]
        x3 = im[48]
        # 左下
        x_half_list3 = [x1[0:32], x2[0:32], x3[0:32]]
        HA_H.append(self.caculate_three_lines(x_half_list3))

        # 右下
        x_half_list4 = [x1[32:64], x2[32:64], x3[32:64]]
        HA_H.append(self.caculate_three_lines(x_half_list4))

        '''竖直半穿越'''
        # 左三列
        y1 = [y[14] for y in im]  # 获取列
        y2 = [y[15] for y in im]
        y3 = [y[16] for y in im]
        # 左上
        y_half_list1 = [y1[0:32], y2[0:32], y3[0:32]]
        VA_H.append(self.caculate_three_lines(y_half_list1))
        # 左下
        y_half_list2 = [y1[32:64], y2[32:64], y3[32:64]]
        VA_H.append(self.caculate_three_lines(y_half_list2))

        # 右三列
        y1 = [y[46] for y in im]  # 获取列
        y2 = [y[47] for y in im]
        y3 = [y[48] for y in im]
        # 右上
        y_half_list3 = [y1[0:32], y2[0:32], y3[0:32]]
        VA_H.append(self.caculate_three_lines(y_half_list3))
        # 右下
        y_half_list4 = [y1[32:64], y2[32:64], y3[32:64]]
        VA_H.append(self.caculate_three_lines(y_half_list4))

        # # 测试打印特征值
        # print im_path
        # print HA
        # print VA
        # print HA_H
        # print VA_H

        # 计算左上角的能量值
        cor_feature.append(self.cor_caculate(im, 0, 16, 0, 16))
        # 计算左下角的能量值
        cor_feature.append(self.cor_caculate(im, 48, 64, 0, 16))
        # 计算右上角的能量值
        cor_feature.append(self.cor_caculate(im, 0, 16, 48, 64))
        # 计算右下角的能量值
        cor_feature.append(self.cor_caculate(im, 48, 64, 48, 64))
        # print cor_feature

        return HA, VA, HA_H, VA_H, cor_feature

    def caculate_line(self, line):
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

    def caculate_three_lines(self, lines):
        # 调用计算单行像素计算方法
        c1 = self.caculate_line(lines[0])
        c2 = self.caculate_line(lines[1])
        c3 = self.caculate_line(lines[2])

        return max(c1, c2, c3)

    def cor_caculate(self, image, t_row, d_row, t_col, d_col):
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

    def write_to_txt(self, ch_name, HA, VA, HA_H, VA_H, cor_feature):
        try:
            fp = open("feature.txt", "a+")
            fp.write(ch_name)
            fp.write(";")

            # for item in HA:
            for i in range(len(HA) - 1):
                fp.write(str(HA[i]) + " ")
            fp.write(str(HA[i + 1]))
            fp.write(",")

            for i in range(len(VA) - 1):
                fp.write(str(VA[i]) + " ")
            fp.write(str(VA[i + 1]))
            fp.write(",")

            for i in range(len(HA_H) - 1):
                fp.write(str(HA_H[i]) + " ")
            fp.write(str(HA_H[i + 1]))
            fp.write(",")

            for i in range(len(VA_H) - 1):
                fp.write(str(VA_H[i]) + " ")
            fp.write(str(VA_H[i + 1]))
            fp.write(",")

            for item in cor_feature:
                fp.write(str(item) + ";")

            fp.write("\n")
            fp.close()

        except IOError:
            print("fail to open value.txt")

    def Cal_all_feas(self):
        for pic_dir in os.listdir(self.calpath):
            for sub_pic_dir in os.listdir(self.calpath + pic_dir + "/"):
                self.caculate_all(pic_dir, sub_pic_dir, self.calpath + pic_dir + "/" + sub_pic_dir + "/")


