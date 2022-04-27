#loading an image with Pillow
from PIL import Image, ImageOps
#from matplotlib import image
#from matplotlib import pyplot
from numpy import asarray
import numpy as np

#image = image.imread('firefirefire.jpg')
#print(f' The data type of this image array is {image.dtype}, which is an 8-bit unsigned integer.')
#print(f' The array is of the following size: {image.shape}, where 3 denotes the RGB channels')

#converting image to greyscale
image = Image.open('firefirefire.jpg').convert('L') 

gray_image = ImageOps.grayscale(image)
gray_image.show()
#image.save('greyfire.jpg')
#showing details about the image
#print(f' The format of the picture is {image.format}.')
#print(f' The pixel size of the image is {image.size}.')
#print(f' The width being {image.width} pixels and the height being {image.height}.')
#print(f' The color scheme is: {image.mode}')

#image.show()

#pyplot.imshow(image)
#pyplot.show()
data = asarray(gray_image)
print(data)
print(np.shape(data))


print(f' The multi-dimensional array shows us the representation of all the brightness of all pixels in the image, .')
print( f' Standard approach for finding the brightest region on an image is to find the 2 dimensional array which sums of the pixels (8 bit image, pixels values from 0 to 255) is the highest')
# Python3 program to find maximum sum
# subarray in a given 2D array



