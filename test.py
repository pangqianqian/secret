import cv2
import os

path = './test'


def main():
    pictures = os.listdir(path)
    for picture in pictures:
        print picture
        pic_path = os.path.join(path, picture)
        #  print pic_path
        im = cv2.imread(pic_path, 0)
        if picture == '6.png':
            print '16', im[17]
            print '32', im[33]
            print '48', im[49]
        else:
            print '16', im[16]
            print '32', im[33]
            print '48', im[48]
        print


if __name__ == '__main__':
    main()
