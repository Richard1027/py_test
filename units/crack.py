# --*-- coding:utf8 --*--

"""
-- author： Richarc --

实现思路：
1、在vectorCompare类中，计算矢量图和字符
2、在build_vector中，截取界面指定元素的图片，获取元素矢量信息，在imageset中获取匹配字符串

"""

from PIL import Image
import os
import math


class vectorCompare:

    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


class build_vector:

    # 在初始化函数中， 将屏幕截图更换为验证码元素截图
    def __init__(self, captcha, element=None):
        self.captcha = captcha
        self.element = element

        left = self.element.location['x']
        top = self.element.location['y']
        right = left + self.element.size['width']
        bottom = top + self.element.size['height']

        im = Image.open(self.captcha)
        im.crop((left, top, right, bottom))
        im.save(self.captcha)

    # 获取验证码字符串
    def store_letters(self):

        v = vectorCompare()
        # 获取im 和 letters
        im, letters = self.get_vector_gifs()
        imageset = self.get_imageset()
        count = 0
        crack_str = ""

        for letter in letters:
            im2 = im.crop((letter[0], 0, letter[1], im.size[1]))
            guess = []
            for img in imageset:
                for x, y in img.items():
                    if len(y) != 0:
                        guess.append((v.relation(y[0], self.get_vectorDict(im2)), x))

            guess.sort(reverse=True)
            crack_str += guess[0][1]
            count += 1
        return crack_str

    # 获取验证码图片RGB
    def get_raw_gif(self):
        im = Image.open(self.captcha)
        im.convert("P")
        im2 = Image.new("P", im.size, 255)

        for x in range(im.size[1]):
            for y in range(im.size[0]):
                pix = im.getpixel((y, x))
                if pix == 220 or pix == 227:
                    im2.putpixel((y, x), 0)
        return im2

    # 获取验证码单个图片矢量图
    def get_vector_gifs(self):
        im = self.get_raw_gif()

        letters = []

        inletter = False
        fountletter = False
        start = 0
        end = 0

        for y in range(im.size[0]):
            for x in range(im.size[1]):
                pix = im.getpixel((y, x))
                if pix != 255:
                    inletter = True

            if fountletter == False and inletter == True:
                fountletter = True
                start = y

            if fountletter == True and inletter == False:
                fountletter = False
                end = y
                letters.append((start, end))

            inletter = False

        return im, letters

    def get_vectorDict(self, im):
        d1 = {}
        count = 0
        for i in im.getdata():
            d1[count] = i
            count += 1
        return d1

    # 根据iconset目录，获取[0-9a-z]中每一个字符的图片矢量信息，然后保存值imageset中
    def get_imageset(self):
        v = vectorCompare()
        iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        imageset = []

        for letter in iconset:
            for img in os.listdir("./iconset/%s/" % (letter)):
                temp = []
                if img != "Thumbs.db" and img != ".DS_Store":
                    temp.append(self.get_vectorDict(Image.open("./iconset/%s/%s" % (letter, img))))
                    imageset.append({letter: temp})
        return imageset

if __name__ == "__main__":
    v = build_vector(captcha="captcha.gif")
    v.store_letters()


