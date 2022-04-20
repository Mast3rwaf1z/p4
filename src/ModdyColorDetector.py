#from PIL import Image
import skimage
import numpy as np

#I1 = Image.open("Image0.png")


def Oldmain(ImageDir):
    Im = skimage.io.imread(ImageDir)
    try:
        RGB = skimage.color.rgba2rgb(Im)
    except ValueError as e:
        RGB = Im
        print(e)
    Lab = skimage.color.rgb2lab(RGB)
    LCH = skimage.color.lab2lch(Lab)
    #Lab2 = np.array(
    #    [[[0.,0.,0.] if (i[0] < 50) and ((i[1] ** 2 + i[2] ** 2) > 3600) and (0.445 < (i[2] / i[1]) < 1.111) else i for i in j] for j
    #     in Lab])
    #Lab2 = np.array(
    #    [[i if (i[0] < 50) and ((i[1] ** 2 + i[2] ** 2) > 3600) and (0.445 < (i[2] / i[1]) < 1.111) else [0.,0.,0.]
    #      for i in j] for j
    #     in Lab])
    Lab2 = np.array([[i if i[0]>55 else (0.,0.,0.) for i in j] for j in Lab])
    #LCH2 = np.array([[i if (i[0]>50) and (i[1]>60) and (0.419<i[2]<0.838) else (0.,0.,0.) for i in j] for j in LCH])
    #LCH2 = np.array([[i if i[0]>55 else (0.,0.,0.) for i in j] for j in LCH])
    RGB2 = skimage.color.lab2rgb(Lab2)
    #RGB2 = np.array([[(i[0]/100,i[0]/100,i[0]/100) for i in j] for j in Lab])
    ax1 = skimage.io.imshow(Im)
    skimage.io.show()
    ax2 = skimage.io.imshow(RGB2)
    skimage.io.show()

def main(ImageDir):
    Im = skimage.io.imread(ImageDir)
    try:
        RGB = skimage.color.rgba2rgb(Im)
    except ValueError as e:
        RGB = Im
        print(e)
    Lab = skimage.color.rgb2lab(RGB)
    Lab2 = np.array([[i if i[0]>55 else (0.,0.,0.) for i in j] for j in Lab])
    RGB2 = skimage.color.lab2rgb(Lab2)
    RGB3 = np.array([[i if i[0]>0.9 and i[2]<0.5 else (0.,0.,0.) for i in j] for j in RGB2])
    #RGB3 = np.array([[i if (i[0] > 0.9 and i[2] < 0.4) or (i[0]>0.9 and i[1]>0.9 and i[2]>0.9) else (0., 0., 0.) for i in j] for j in RGB2])
    ax1 = skimage.io.imshow(Im)
    skimage.io.show()
    #ax2 = skimage.io.imshow(RGB2)
    #skimage.io.show()
    ax3 = skimage.io.imshow(RGB3)
    skimage.io.show()

def test():
    Im = skimage.io.imread("Image1.png")
    RGB = skimage.color.rgba2rgb(Im)
    Lab = skimage.color.rgb2lab(RGB)
    LCH = skimage.color.lab2lch(Lab)
    count = 0
    for j in LCH:
        for i in j:
            if i[0]>50:
                print(i)
            #if (i[0] > 50) and ((i[1] ** 2 + i[2] ** 2) > 3600) and (0.445 < (i[2] / i[1]) < 1.111):
            #    count+=1
            #    print(i)
    print(count)

def AllImagemain():
    for i in range(1,8):
        if i>1 or i<6:
            main(f'Image{i}.jpg')
        else:
            main(f'Image{i}.png')

if __name__ == "__main__":
    main("../ModdyImages/Image1.png")
    #AllImagemain()
    #test()

# Image 1 works good with red>90% and blue<90%
# Image 2 works good with red>90% and blue<50%
# Image 3 works good with red>90% and blue<80%
# Image 4 works good with red>90% and blue<40% Does not detect the fire behind the smoke
# Image 5 works good with red>90% and blue<50%

