import cv2 as cv
import numpy as np


def detect_fire(image:cv.Mat) -> tuple[bool, cv.Mat]:
    #image = cv.imread("wildfire.jpg")
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HLS)                  # Converting BGR color scheme to HSV
    #print(hsv.shape)

    # defining lower mask (red has lower hue values 0-10)
    lower_red = np.array([0,50,50])                         # Hue, saturation, value, in the array
    upper_red = np.array([10,255,255])
    

    # Threshold the HSV image to get only blue colors
    mask0 = cv.inRange(hsv, lower_red, upper_red)

    #upper mask (red has hue values 170-180)
    lower_red1 = np.array([170,100,50])
    upper_red1 = np.array([180,255,255])
    mask1 = cv.inRange(hsv,lower_red1, upper_red1)

    mask = mask0+mask1    

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(image,image, mask= mask)
    #cv.imshow('image',image)
    #cv.imshow('mask',mask)
    #cv.imshow('res',res)

    all_pixels = res.size
    red_pixels = np.count_nonzero(res)
    percentage = round(red_pixels * 100 / all_pixels, 2)


    

    #if there are any white pixels on mask, sum will be > 0
    red_detected = np.sum(mask1)
    #yellow_detected = np.sum(mask2)
    data = (all_pixels, red_pixels, percentage)
    if red_detected > 0 and percentage < 1: 
        #print('Potential fire detected!')
        return True, res, data
    else: 
        #print('No fire detected..')
        return False, res, data


if __name__ == "__main__":
    from sys import argv
    from os import chdir, path
    chdir(path.dirname(argv[0])) #change directory to script location

    if len(argv) > 1:
        image = cv.imread(argv[1])
    else:
        image = cv.imread("../images/smallfire.jpg")

    _, res, data = detect_fire(image)
    print("Total amount of pixels in the image: " + str(data[0]))
    print("Amount of red pixels in the image: " + str(data[1]))  
    print("Percentage of red pixels: " + str(data[2]) + "%")