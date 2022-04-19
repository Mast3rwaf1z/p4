import cv2 as cv
import numpy as np

def main(Image):
    #image = cv.imread("wildfire.jpg")
    image = cv.imread(Image)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)                  # Converting BGR color scheme to HSV
    print(hsv.shape)

    # defining lower mask (red has lower hue values 0-10)
    #lower_red = np.array([0,50,50])                         # Hue, saturation, value, in the array
    #upper_red = np.array([10,255,255])
    

    # Threshold the HSV image to get only blue colors
    #mask0 = cv.inRange(hsv, lower_red, upper_red)

    #upper mask (red has hue values 170-180)
    lower_red1 = np.array([170,100,50])
    upper_red1 = np.array([180,255,255])
    mask1 = cv.inRange(hsv,lower_red1, upper_red1)

    #mask = mask0+mask1    

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(image,image, mask= mask1)
    cv.imshow('image',image)
    #cv.imshow('mask',mask)
    cv.imshow('res',res)

    #if there are any white pixels on mask, sum will be > 0
    red_detected = np.sum(mask1)
    #yellow_detected = np.sum(mask2)
    if red_detected > 0:
        print('Potential fire detected!')
    else: 
        print('No fire detected..')


    cv.waitKey()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main("smallfire.jpg")