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
        '''
        三行取最大值
        '''
        # 水平全穿越
        xlist1=im[14:17]
        HA.append(caculate_three_lines(xlist1))
        xlist2=im[30:33]
        HA.append(caculate_three_lines(xlist2))
        xlist3=im[46:49]
        HA.append(caculate_three_lines(xlist3))

        # 竖直全穿越
        y1 = [y[14] for y in im]  # 获取三列
        y2 = [y[15] for y in im]  
        y3 = [y[16] for y in im]  
        ylist1=[y1,y2,y3]
        VA.append(caculate_three_lines(ylist1))

        y1 = [y[30] for y in im]  # 获取三列
        y2 = [y[31] for y in im]  
        y3 = [y[32] for y in im]  
        ylist2=[y1,y2,y3]
        VA.append(caculate_three_lines(ylist2))

        y1 = [y[46] for y in im]  # 获取三列
        y2 = [y[47] for y in im]  
        y3 = [y[48] for y in im]  
        ylist3=[y1,y2,y3]
        VA.append(caculate_three_lines(ylist3))
        
        '''水平半穿越'''
        #上三行像素
        x1 = im[14]
        x2 = im[15]
        x3 = im[16]
        #左上
        x_half_list1 =[x1[0:32],x2[0:32],x3[0:32]]
        
        HA_H.append(caculate_three_lines(x_half_list1))
        #右上
        x_half_list2 =[x1[32:64],x2[32:64],x3[32:64]]        
        HA_H.append(caculate_three_lines(x_half_list2))
        
        #下三行像素
        x1 = im[46]
        x2 = im[47]
        x3 = im[48]
        #左下
        x_half_list3 =[x1[0:32],x2[0:32],x3[0:32]]        
        HA_H.append(caculate_three_lines(x_half_list3))
        
        #右下
        x_half_list4 =[x1[32:64],x2[32:64],x3[32:64]]        
        HA_H.append(caculate_three_lines(x_half_list4))

        '''竖直半穿越'''
        #左三列
        y1 = [y[14] for y in im]  # 获取列
        y2 = [y[15] for y in im]
        y3 = [y[16] for y in im]
        #左上
        y_half_list1 = [y1[0:32],y2[0:32],y3[0:32]]
        VA_H.append(caculate_three_lines(y_half_list1))
        #左下
        y_half_list2 = [y1[32:64],y2[32:64],y3[32:64]]
        VA_H.append(caculate_three_lines(y_half_list2))

        #右三列
        y1 = [y[46] for y in im]  # 获取列
        y2 = [y[47] for y in im]
        y3 = [y[48] for y in im]
        #右上
        y_half_list3 = [y1[0:32],y2[0:32],y3[0:32]]
        VA_H.append(caculate_three_lines(y_half_list3))
        #右下
        y_half_list4 = [y1[32:64],y2[32:64],y3[32:64]]
        VA_H.append(caculate_three_lines(y_half_list4))

        
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

'''
三行像素，取最大的穿越值

一：15,16,17
二：31,32,33
三：47,48,49
'''
def caculate_three_lines(lines):
    #调用计算单行像素计算方法
    c1=caculate_line(lines[0])
    c2=caculate_line(lines[1])
    c3=caculate_line(lines[2])

    return max(c1,c2,c3)


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
        fp = open("num_value.txt", "a+")
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
    caculate_all('./res_number')
