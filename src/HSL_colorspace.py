from time import perf_counter
import cv2 as cv
import numpy as np

from coordinate_detection import get_coords


def main(Image):
    #image = cv.imread("wildfire.jpg")
    image = cv.imread(Image)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HLS)                  # Converting BGR color scheme to HSV
    print(hsv.shape)

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

    return res


if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        res = argv[1]
    else:
        res = main("smallfire.jpg")
    pre = perf_counter()
    gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    matrix = [[gray[y][x] for x in range(len(gray[y]))] for y in range(len(gray))]
    num_fires, sizes, coordinates, _ = get_coords(matrix)
    post = perf_counter()
    
    print(f'Number of fires:        {num_fires}')
    print(f'size of fires:          {sizes}')
    print(f'coordinate of fires:    {coordinates}')
    print(f'time:                   {post-pre}')