# coding:utf8
'''
功能：将工商营业执照图切割成一张张文字图片（保存企业名称和企业注册号)
'''

import cv2
import math
import os


class Cutfonts:
    def __init__(self, pic_path):
        self.pic_dir = pic_path + "/"
        self.result_dir = "./r/"

    def Qushuiyin(self, grayimage, height, width):
        ret, thresh = cv2.threshold(grayimage, 220, 255, cv2.THRESH_BINARY_INV)
        # cv2.imwrite("shuiyin.png",thresh)

        for i in range(0, height):
            for j in range(0, width):
                if thresh[i, j] < 255:
                    grayimage[i, j] = 0
        # cv2.imwrite("qushuiyin.png",grayimage)

        # 腐蚀
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        grayimage = cv2.erode(grayimage, kernel)
        # cv2.imwrite("erode.png",grayimage)
        return grayimage

    def cutlines(self, thresh, linebegin, height):
        fh = lh = 0
        # 先切一行，first和last用来标记是否已取得一行开始与结束位置
        first = False
        last = False
        for i in range(linebegin, height):
            if first and last:
                break
            for j in range(0, 100):
                if thresh[i, j] == 0:
                    if not first:
                        fh = i
                        first = True
                        break
                    elif first and not last:
                        break
                elif first and j == 99:
                    lh = i
                    last = True
        return (fh, lh)

    # 一次遍历，找空白段，找到标点符号位置
    def findblank(self, line, fh, lh, width):
        first = False
        last = False
        lineh = lh - fh + 2
        blanks = []
        for i in range(0, width):
            for j in range(0, lineh):
                if line[j, i] == 0:
                    if first:
                        lw = i
                        first = False
                        blanks.append(lw - fw)
                    break
                elif j == lineh - 1:
                    if not first:
                        fw = i
                        first = True
        # 空白段排序，最小的是字体间间隔，其次是标点符号前后空格
        blanks.sort()
        if len(blanks) > 0:
            font_blank = blanks[0]
        else:
            font_blank = 0
        char_blank = 0

        for i in range(len(blanks)):
            if (blanks[i] - font_blank > 6 * font_blank):
                char_blank = blanks[i]
                break
        return char_blank

    # 二次遍历，进行切分，按列查找，有黑点即为开始，全白或黑点比例小于0.1的位置
    def cutfonts(self, line, fh, lh, width):
        lines = []
        length = []
        lensum = 0
        lineh = lh - fh + 2
        first = False
        last = False
        # font=0

        # print(lineh)
        # print("the length of cut result:")
        for i in range(0, width):
            for j in range(0, lineh):
                if line[j, i] == 0:
                    if not first:
                        fw = i
                        first = True
                        break
                    elif first and not last:
                        break
                elif first and j == lineh - 1:
                    lw = i
                    last = True
            if first and last:
                first = False
                last = False
                if fw == lw:
                    continue
                lines.append((fw, lw))
                length.append(lw - fw)
                lensum = lensum + (lw - fw)
                # print(fw,lw)
        return (lines, length, lensum)

    # 找到分号位置，分成两部分
    def divideparts(self, lines, char_blank):
        divide = 0
        for l in range(len(lines) - 1):
            (fa, la) = lines[l]
            (fb, lb) = lines[l + 1]
            if fb - la > char_blank and fb - la - char_blank < char_blank / 2:
                divide = l + 1
                break
        # print("divide",divide)

        return divide

    # 前后两部分分别切分或合并
    def hebing(self, lines, length, lensum, divide):
        subsum = 0
        for l in range(0, divide):
            subsum = subsum + length[l]
        # print("subsum",subsum,lensum,(lensum-subsum)/(len(length)-divide))

        divide = divide - 1

        sublength = length[:divide]
        sublength.sort()

        # 前后两部分分别切分或合并
        result = []
        l = 0
        while l < len(length):
            if l == 0:
                # avglen=subsum/(divide+1)
                avglen = sublength[divide / 2]
                # print(avglen)
            elif l == divide:
                # avglen=(lensum-subsum)/(len(length)-divide-1)
                sublength = length[divide + 1:]
                sublength.sort()
                print(len(length), len(sublength), divide)
                avglen = sublength[len(sublength) - 1 - len(sublength) / 4]
                (positionb, positione) = lines[l]
                # print(avglen)
                l = l + 1
                continue
            # 块比较小
            if abs(length[l] - avglen) > avglen / 3 and length[l] < avglen:
                begin = l
                sublen = length[l]
                # while l<len(length) and abs(length[l]-avglen)>avglen/3 and length[l]<avglen:
                # while l<len(length)-1 and abs(sublen-avglen)>avglen/3:
                while l < len(length) - 1 and sublen + length[l + 1] < avglen:
                    l = l + 1
                    sublen = sublen + length[l]

                # 后面有小的块，合并起来
                if l - begin > 0:
                    (fa, la) = lines[begin]
                    (fb, lb) = lines[l]
                    result.append((fa, lb))
                # 块小但也没有很小，附近也没有小的块，保存
                else:
                    result.append(lines[l])
            # 块比较大
            elif abs(length[l] - avglen) > avglen / 3 and length[l] > avglen:
                subcount = math.floor(float(length[l]) / float(avglen))
                if subcount > 0:
                    sublen = int(math.floor(length[l] / subcount))
                # print("cut",sublen)
                (fa, la) = lines[l]
                for sub in range(0, int(subcount)):
                    result.append((fa, fa + sublen))
                    fa = fa + sublen
            # 块不大不小直接保存
            else:
                result.append(lines[l])
            l = l + 1
        return result, positionb

    def bor_chinese(self, im):
        '''
        对二值化后的图片进行边框提取
        :return:
        '''
        posup = 0
        posdown = 0
        posleft = 0
        posright = 0
        flag = 0

        # width = len(im[0])
        # height = len(im)
        height = im.shape[0]
        width = im.shape[1]
        # print("im",width,height)
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
        # print("pos",posup,posdown,posleft,posright)
        im2 = im[posup:posdown + 1, posleft:posright + 1]

        return im2

    def Cut_all(self):
        count = 0
        if not os.path.exists(self.result_dir):
            os.mkdir(self.result_dir)
        for fileName in os.listdir(self.pic_dir):
            count = count + 1
            print(count)
            save_dir_name = os.path.splitext(fileName)[0]
            save_dir = self.result_dir + save_dir_name + "/"
            save_num_dir = save_dir + "num/"
            save_name_dir = save_dir + "name/"
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            if not os.path.exists(save_num_dir):
                os.mkdir(save_num_dir)
            if not os.path.exists(save_name_dir):
                os.mkdir(save_name_dir)
            src = cv2.imread(self.pic_dir + fileName)

            height = src.shape[0]
            width = src.shape[1]
            # print(height,width)
            grayimage = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            qushuiyin = self.Qushuiyin(grayimage, height, width)
            # 二次二值化
            ret, thresh = cv2.threshold(qushuiyin, 6, 255, cv2.THRESH_BINARY_INV)

            height = thresh.shape[0]
            width = thresh.shape[1]
            # print(height,width)
            newlinebegin = 0
            font = 1
            for linenum in range(0, 2):
                font = 1
                if linenum == 0:
                    save_dir = save_num_dir
                else:
                    save_dir = save_name_dir
                (fh, lh) = self.cutlines(thresh, newlinebegin, height)
                line = thresh[fh:lh + 2, 0:width]
                char_blank = self.findblank(line, fh, lh, width)
                (lines, length, lensum) = self.cutfonts(line, fh, lh, width)
                divide = self.divideparts(lines, char_blank)
                if divide == 0:
                    print("divide")
                    continue
                (result, pb) = self.hebing(lines, length, lensum, divide)
                for l in range(len(result)):
                    (fa, fb) = result[l]
                    if fa < pb:
                        continue
                    subline = line[0:lh - fh, fa:fb]
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
                    subline = cv2.erode(subline, kernel)
                    subline = self.bor_chinese(subline)
                    if linenum == 1 and fb - fa < 10:
                        retval, subline = cv2.threshold(subline, 127, 255, cv2.THRESH_BINARY)
                        cv2.imwrite(save_dir + str(font) + ".png", subline)
                    else:
                        subline = cv2.resize(subline, (64, 64))
                        retval, subline = cv2.threshold(subline, 127, 255, cv2.THRESH_BINARY)
                        cv2.imwrite(save_dir + str(font) + ".png", subline)
                    font = font + 1
                newlinebegin = lh
