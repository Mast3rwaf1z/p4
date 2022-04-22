import cv2 as cv
import numpy as np


def main(Image):
    image = cv.imread(Image)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)                  # Converting BGR color scheme to HSV
    rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    print(hsv.shape)

    # defining lower mask (red has lower hue values 0-10)
    #lower_red = np.array([0,50,50])                         # Hue, saturation, value, in the array
    #upper_red = np.array([10,255,255])
    

    # Threshold the HSV image to get only blue colors
    #mask0 = cv.inRange(hsv, lower_red, upper_red)

    #upper mask (red has hue values 170-180)
    lower_red = np.array([160,0,0])
    upper_red = np.array([255,100,100])
    mask1 = cv.inRange(rgb,lower_red, upper_red)


    #mask = mask0+mask1    

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(rgb, rgb, mask= mask1)
    cv.imshow('image',image)
    #cv.imshow('mask',mask)
    cv.imshow('res',cv.cvtColor(res, cv.COLOR_RGB2BGR))

    all_pixels = res.size
    red_pixels = np.count_nonzero(res)
    percentage = round(red_pixels * 100 / all_pixels, 2)
    


    print("Total amount of pixels in the image: " + str(all_pixels))
    print("Amount of red pixels in the image: " + str(red_pixels))  
    print("Percentage of red pixels: " + str(percentage) + "%")




    #if there are any white pixels on mask, sum will be > 0
    red_detected = np.sum(mask1)
    #yellow_detected = np.sum(mask2)
    if red_detected > 0 and percentage < 1: 
        print('Potential fire detected!')
    else: 
        print('No fire detected..')



    cv.waitKey()
    cv.destroyAllWindows()



if __name__ == "__main__":
    from sys import argv
    if len(argv) >= 2:
        for i in range(1,len(argv)):
            main(argv[i])
    else:
        main("smallfire.jpg")


    