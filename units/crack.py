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

    def __init__(self, captcha):
        self.captcha = captcha

    def store_letters(self):

        v = vectorCompare()
        # 获取im 和 letters
        im, letters = self.get_vector_gifs()
        imageset = self.get_imageset()

        count = 0
        for letter in letters:
            #str_time = time.strftime("%y%m%d%H%M%S")
            #m = hashlib.md5()
            im2 = im.crop((letter[0], 0, letter[1], im.size[1]))
            guess = []
            for img in imageset:
                for x, y in img.items():
                    if len(y) != 0:
                        guess.append((v.relation(y[0], self.get_vectorDict(im2)), x))

            guess.sort(reverse=True)
            print("", guess[0])
            count += 1

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


