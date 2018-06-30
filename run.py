# coding:utf8
'''
功能：进行识别
'''

import os
import xlwt
import cv2
from Cal_fea import Calfea
from Database import Database
import sys

reload(sys)
sys.setdefaultencoding('utf8')

pic_dir = "./result"
save_dir = './result.xls'

# 建立数据库链接
database = Database()
db = database.connectdb()
calfea = Calfea()


def main():
    '''
    读取图片文字并写入excel
    :return:
    '''
    # 识别写入excel
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

        # filename = subpicture.split('.')[0]
        # print filename

        for subfile in file:
            str2 = os.path.join(str1, subfile)
            cell = os.listdir(str2)  # 每个文字或数字单元
            num = len(cell)
            l = dict()
            if subfile == 'name':  # 企业名称
                col = 0  # 列
                k1 = k2 = 0
                flag = True
                for subcell in cell:
                    str3 = os.path.join(str2, subcell)
                    im = cv2.imread(str3)
                    pos = subcell.split('.')[0]
                    if im.shape[0] != 64 and flag == True:
                        word = "!"
                        k1 = int(pos) - 1
                        flag = False
                    elif im.shape[0] != 64 and flag == False:
                        word = "!"
                        k2 = int(pos) - 1
                    else:
                        word = map(str3, 0)
                    dic = {int(pos) - 1: word}
                    l.update(dic)
                if k2 != 0:
                    if k1 < k2:
                        dic1 = {k1: "("}
                        dic2 = {k2: ")"}
                    else:
                        dic1 = {k2: "("}
                        dic2 = {k1: ")"}
                    l.update(dic1)
                    l.update(dic2)
                l.update({num - 1: "司"})
                l.update({num - 2: "公"})
                l.update({num - 3: "限"})
                l.update({num - 4: "有"})
            else:  # 企业数字
                col = 1  # 列
                for subcell in cell:
                    str3 = os.path.join(str2, subcell)
                    word = map(str3, 1)
                    pos = subcell.split('.')[0]
                    dic = {int(pos) - 1: word}
                    l.update(dic)

            # 将字符串汇总
            words = ''
            for i in range(num):
                words += l[i]
            # 写入excel
            sheet.write(row, col, words)
        row += 1

    excel.save(save_dir)
    print '写入表格成功！'


def map(im_path, flag):
    '''
    flag=0,匹配中文
    flag=1,匹配数字和英文
    :param im:
    :return:
    '''
    try:
        feature = calfea.caculate(im_path)
        s = ''
        for f in feature[:4]:
            for item in f:
                s += str(item) + " "
            s += ","
        for item in feature[4]:
            s += str(item) + " "
        if flag == 1:
            return database.querydb(db, s, 1)
        else:
            return database.querydb(db, s, 0)
    except:
        return '!'


if __name__ == '__main__':
    main()
    database.closedb(db)
