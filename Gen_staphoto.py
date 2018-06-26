# encoding: utf-8
'''
功能:生成标准字库图片
'''
import os
import pygame
import codecs


class Gen_staphoto:
    def readtxt(self):
        dic = []
        with codecs.open('常用字3750.txt', 'r', 'utf-8') as f:
            lines = f.readlines()
            for line in lines:
                for word in line[:-1]:
                    dic.append(word)
        f.close
        return dic

    def gen_chinese(self):
        pygame.init()
        start, end = (0x005a, 0x005b)  # 汉字编码范围
        for codepoint in range(int(start), int(end)):
            word = unichr(codepoint)
            font = pygame.font.Font("微软vista雅黑.ttf", 64)
            # 当前目录下要有微软雅黑的字体文件msyh.ttc,或者去c:\Windows\Fonts目录下找
            # 64是生成汉字的字体大小
            rtext = font.render(word, True, (0, 0, 0), (255, 255, 255))
            pygame.image.save(rtext, os.path.join('./temp/english/', word + ".png"))
        print '生成汉字库成功！'
