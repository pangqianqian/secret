# coding:utf8

import os
import xlwt
import pytesseract
from PIL import Image
import cv2

pic_dir = "./result"
save_dir = './result.xls'


def main():
    '''
    读取图片文字并写入excel
    :return:
    '''

    excel = xlwt.Workbook(encoding='utf-8')  # 创建一个Excel
    sheet = excel.add_sheet('Sheet1')  # 在其中创建一个名为hello的sheet
    sheet.write(0, 0, u'企业名称')  # 往sheet里第一行第一列写一个数据
    sheet.write(0, 1, u'企业注册号')  # 往sheet里第二行第一列写一个数据
    # 照片
    picture = os.listdir(pic_dir)
    row = 1  # 行
    for subpicture in picture:  # 依次对每张照片进行处理
        str1 = os.path.join(pic_dir, subpicture)  # 文件名
        file = os.listdir(str1)  # file 为name或num
        for subfile in file:
            str2 = os.path.join(str1, subfile)
            cell = os.listdir(str2)  # 每个文字或数字单元
            num = len(cell)
            l = []
            if subfile == 'name':  # 企业名称
                col = 0  # 列
                for subcell in cell:
                    str3 = os.path.join(str2, subcell)
                    word = map(str3, 0)
                    pos = subcell.split('.')[0]
                    l.insert(int(pos), word)
            else:  # 企业数字
                col = 1  # 列
                for subcell in cell:
                    str3 = os.path.join(str2, subcell)
                    word = map(str3, 1)
                    pos = subcell.split('.')[0]
                    l.insert(int(pos), word)
            # 将字符串汇总
            words = ''
            for i in range(num):
                words += l[i]
            print words
            # 写入excel
            sheet.write(row, col, words)
        row += 1

    excel.save(save_dir)


def map(im_path, flag):
    '''
    flag=0,匹配中文
    flag=1,匹配数字和英文
    :param im:
    :return:
    # '''
    if flag == 1:
        return '1'
    else:
        im = cv2.imread(im_path)
        if len(im[0]) != 64:
            return '('
        else:
            img = Image.open(im_path)
            data = pytesseract.image_to_string(img, lang='chi_sim')
            return data
    # if flag == 1:
    #     return '1'
    # else:
    #     return '阿'


if __name__ == '__main__':
    main()