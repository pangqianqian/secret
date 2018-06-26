# coding:utf8
'''
功能：选择工商图片路径和excel表格路径
'''
from Tkinter import *
import tkFileDialog
import sys
from Cut_fonts import Cutfonts
from Cal_fea import Calfea

reload(sys)
sys.setdefaultencoding("utf-8")


class App:
    def __init__(self, master):
        # 构造函数里传入一个父组件(master),创建一个Frame组件并显示
        frame = Frame(master)
        frame.pack()
        self.message = Label(frame, text="执照图片路径").grid(column=1, row=1, sticky=W)
        # self.message.pack(side=TOP)
        self.showpath = Entry(frame, textvariable=path).grid(column=1, row=2, sticky=W)
        # self.message.pack(side=TOP)
        self.choose = Button(frame, text="浏览", command=self.selectPath).grid(column=3, row=2, sticky=W)
        # 创建两个button，并作为frame的一部分
        self.yes = Button(frame, text="确认", command=self.ret_path).grid(column=1, row=3, sticky=W)
        # self.yes.pack(side=LEFT) #此处side为LEFT表示将其放置 到frame剩余空间的最左方
        self.pause = Button(frame, text="取消", command=frame.quit).grid(column=2, row=3, sticky=W)
        # self.pause.pack(side=LEFT)

    def ret_path(self):
        # path=self.showpath.text
        print(path.get())
        cutfonts = Cutfonts(path.get())
        cutfonts.Cut_all()
        # calfeature = Calfea()
        # calfeature.Cal_all_feas()

    def selectPath(self):
        path_ = tkFileDialog.askdirectory()
        path.set(path_)

    def run(self):
        win.mainloop()


win = Tk()
path = StringVar()
app = App(win)
# win.geometry("400x300+0+0")
win.mainloop()
