from time import perf_counter
import cv2 as cv
import numpy as np
from multiprocessing import  Pool

def process_line(values:cv.Mat):
    return np.array([255 if pixel[2] > 165 and pixel[1] < 100 and pixel[0] < 100 else 0 for pixel in values])

def process_line_ir(values):
    return np.array([255 if pixel[0] > 200 else 0 for pixel in values])

def fire_detection_algorithm(image:cv.Mat, color_type:str) -> tuple[bool, np.ndarray, tuple[int, int, float]]:
    #image = cv.imread("wildfire.jpg")
    color_type = color_type.lower()
    if color_type == "hsl":
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
        result = np.array([[tmp[i][j][0] for j in range(len(tmp[i]))] for i in range(len(tmp))])
    elif color_type == "rgb":
        result = np.array([[255 if image[i][j][2] > 165 and image[i][j][1] < 100 and image[i][j][0] < 100 else 0 for j in range(len(image[i]))] for i in range(len(image))])
    elif color_type == "pool_rgb":
        with Pool(4) as p:
            result = np.array(p.map(process_line, [row for row in image]))

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
        return False, result, data

def detect_fire_ir(rgb_image:cv.Mat, ir_image:cv.Mat):
    with Pool(4) as p:
        ir_result = np.array(p.map(process_line_ir, [row for row in ir_image]))

    with Pool(4) as p:
        rgb_result = np.array(p.map(process_line, [row for row in rgb_image]))
    
    result = np.array([[255 if ir_pixel != 0 and rgb_pixel != 0 else 0 for ir_pixel, rgb_pixel in zip(ir_row, rgb_row)] for ir_row, rgb_row in zip(ir_result, rgb_result)])
    all_pixels = np.sum(len(row) for row in result)
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
        return False, result, data

if __name__ == "__main__":
    from sys import argv
    from os import chdir, path

    if len(argv) > 1:
        image = cv.imread(argv[1])
    else:
        chdir(path.dirname(argv[0])) #change directory to script location
        image = cv.imread("../images/smallfire.jpg")
    hsl_pre = perf_counter()
    _, result, data = fire_detection_algorithm(image, "hsl")
    hsl_post = perf_counter()
    
    rgb_pre = perf_counter()
    _, rgb, data = fire_detection_algorithm(image, "rgb")
    rgb_post = perf_counter()

    rgb_pool_pre = perf_counter()
    _, pool, data = fire_detection_algorithm(image, "pool_rgb")
    rgb_pool_post = perf_counter()

    print("Total amount of pixels in the image: " + str(data[0]))
    print("Amount of red pixels in the image: " + str(data[1]))  
    print("Percentage of red pixels: " + str(data[2]) + "%")
    print(f'hsl time:       {hsl_post-hsl_pre}')
    print(f'rgb time:       {rgb_post-rgb_pre}')
    print(f'rgb+pool time:  {rgb_pool_post-rgb_pool_pre}')
    for i in range(len(result)):
        for j in range(len(result[i])):
            assert rgb[i][j] == pool[i][j]# if true the algorithm is calculating correctly