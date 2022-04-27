from time import perf_counter
import cv2 as cv
import numpy as np
try:
    from modules.get_channel import get_channel
except:
    from get_channel import get_channel


def detect_fire(image:cv.Mat, color_type:str) -> tuple[bool, list[list[int]]]:
    #image = cv.imread("wildfire.jpg")
    match color_type.lower():
        case "hsl":
            hsl = cv.cvtColor(image, cv.COLOR_BGR2HLS) # Converting BGR color scheme to HSV
            # defining lower mask (red has lower hue values 0-10)
            lower_red0 = np.array([0,50,50]) # Hue, saturation, value
            upper_red0 = np.array([10,255,255])
            #upper mask (red has hue values 170-180)
            lower_red1 = np.array([170,50,50])
            upper_red1 = np.array([180,255,255])
            mask0 = cv.inRange(hsl, lower_red0, upper_red0) # Threshold the HSV image to get only blue colors
            mask1 = cv.inRange(hsl, lower_red1, upper_red1)
            mask = mask0+mask1
            tmp = cv.bitwise_and(hsl, hsl, mask=mask) # Bitwise-AND mask and original image
            result = [[tmp[i][j][0] for j in range(len(tmp[i]))] for i in range(len(tmp))]
        case "hsv":
            hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
            lower_red = np.array([0,50,50])
            upper_red = np.array([10,255,255])
            mask = cv.inRange(hsv, lower_red, upper_red)
            result = cv.bitwise_and(image, image, mask=mask) 
        case "rgb":
            blue  = get_channel(image, 0)
            green = get_channel(image, 1)
            red   = get_channel(image, 2)
            result = [[255 if red[i][j] > 165 and green[i][j] < 100 and blue[i][j] < 100 else 0 for j in range(len(image[i]))] for i in range(len(image))]

    all_pixels = sum([len(result[i]) for i in range(len(result))])
    red_pixels = np.count_nonzero(result)
    percentage = round(red_pixels * 100 / all_pixels, 2)


    #if there are any white pixels on mask, sum will be > 0
    red_detected = np.sum(result)
    #yellow_detected = np.sum(mask2)
    data = (all_pixels, red_pixels, percentage)
    if red_detected > 0 and percentage < 1:
        #print('Potential fire detected!')
        return True, result, data
    else: 
        #print('No fire detected..')
        return False, [[result[i][j] for j in range(len(result[i]))] for i in range(len(result))], data


if __name__ == "__main__":
    from sys import argv
    from os import chdir, path

    if len(argv) > 1:
        image = cv.imread(argv[1])
    else:
        chdir(path.dirname(argv[0])) #change directory to script location
        image = cv.imread("../images/smallfire.jpg")
    hsl_pre = perf_counter()
    _, res, data = detect_fire(image, "hsl")
    hsl_post = perf_counter()
    rgb_pre = perf_counter()
    detect_fire(image, "rgb")
    rgb_post = perf_counter()
    print("Total amount of pixels in the image: " + str(data[0]))
    print("Amount of red pixels in the image: " + str(data[1]))  
    print("Percentage of red pixels: " + str(data[2]) + "%")
    print(f'hsl time:   {hsl_post-hsl_pre}')
    print(f'rgb time:   {rgb_post-rgb_pre}')