import cv2 as cv
import numpy as np

image = cv.imread("wildfire.jpg")
#image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

#(R,G,B) = cv.split(image)
mask1 = cv.inRange(image, (0, 0, 50), (50, 50,255))  #colour values to represent specific color in the RGB color scheme - here red
#mask2 = cv.inRange(image, (0, 50, 0), (45, 255,255)) # here green

#mask = cv.bitwise_or(mask1, mask2)
#target = cv.bitwise_and(image,image, mask=mask)

target = cv.bitwise_or(image,image, mask=mask1)

#create named windows for each of the images we are going to display
#cv.namedWindow("Blue", cv.WINDOW_NORMAL)
#cv.namedWindow("Green", cv.WINDOW_NORMAL)
#cv.namedWindow("Red", cv.WINDOW_NORMAL)                     #display the images
#cv.imshow("Blue",B)
#cv.imshow("Green", G)
#cv.imshow("Red", R)
cv.imshow('mask red color',mask1)
#cv.imshow('mask green color',mask2)
#cv.imshow('mask of both colors',mask)
cv.imshow('target colors extracted',target)

#write the images to disk
#cv.imwrite("channel_red.jpg", R)
#cv.imwrite("channel_green.jpg", G)
#cv.imwrite("channel_blue.jpg", B)
cv.imwrite("mask red color.jpg", mask1)
#cv.imwrite("mask green color.jpg", mask2)
#cv.imwrite("mask red and green color.jpg", mask)
cv.imwrite("extracted_colors.jpg", target)

#if there are any white pixels on mask, sum will be > 0
red_detected = np.sum(mask1)
#yellow_detected = np.sum(mask2)
if red_detected > 0:
    print('Potential fire detected!')
else: 
    print('No fire detected..')

if cv.waitKey(0):
    cv.destroyAllWindows()