from time import perf_counter
import cv2 as cv
import numpy as np
from threading import Thread
from multiprocessing import  Pool, Queue
try:
    from modules.get_channel import get_channel
except:
    from get_channel import get_channel

def return_var(function, results, index):
    results[index] = function()

def mp_return(function, results:Queue):
    results.put(function())
    print()


def get_channel_from_index(data:tuple[cv.Mat, int]):
    return get_channel(data[0], data[1])

def process_line(values:tuple[np.ndarray]):
    return np.array([255 if values[2][i] > 165 and values[1][i] < 100 and values[0][i] < 100 else 0 for i in range(len(values[0]))])

def process_line_ir(values:tuple[np.ndarray]):
    return np.array([255 if values[2][i] > 200 else 0 for i in range(len(values[0]))])

def detect_fire(image:cv.Mat, color_type:str) -> tuple[bool, np.ndarray, tuple[int, int, float]]:   # defining image input: image name, color space, setting return data types
    color_type = color_type.lower()                                                                 # color_type set to not case-sensitive
    if color_type == "hsl":                                              
        hsl = cv.cvtColor(image, cv.COLOR_BGR2HLS)                                                  # converting BGR to HSL color scheme (Hue, saturation, lightness)
        lower_red0 = np.array([0,50,50])                                                            # defining lower mask values (red has lower hue values 0-10)
        upper_red0 = np.array([10,255,255])
        lower_red1 = np.array([170,50,50])                                                          # defining upper mask values (red has upper hue values 170-180)
        upper_red1 = np.array([180,255,255])
        mask0 = cv.inRange(hsl, lower_red0, upper_red0)                                             # masking color range with threshold for the lower mask values
        mask1 = cv.inRange(hsl, lower_red1, upper_red1)                                             # masking color range with threshold for the upper mask values
        mask = mask0+mask1                                                                          # defining complete mask thresholds
        tmp = cv.bitwise_and(hsl, hsl, mask=mask)                                                   # Bitwise-and: Calculates the per-element bit-wise conjunction of two arrays or an array and a scalar.  
        result = np.array([[tmp[i][j][0] for j in range(len(tmp[i]))] for i in range(len(tmp))])    # Converting OpenCV array to NumPy array 
    elif color_type == "rgb":                                                             
        blue  = get_channel(image, 0)                                                               # extracting blue color channel
        green = get_channel(image, 1)                                                               # extracting green color channel
        red   = get_channel(image, 2)                                                               # extracting red color channel
        #below: setting red values to white (value 255) & everything else to black (value 0)                                                                                    
        result = np.array([[255 if red[i][j] > 165 and green[i][j] < 100 and blue[i][j] < 100 else 0 for j in range(len(image[i]))] for i in range(len(image))]) 
    elif color_type == "pool_rgb":                                                                  # multiprocessing function
        with Pool(3) as p:                                                                          # Using 3 cores, starting 3 processes with pool
            results = p.map(get_channel_from_index, [(image, 0),(image, 1),(image, 2)])             # Using pool.map() to extracting RGB color channels in parallel 
        with Pool(4) as p:                                                                          # Using 4 cores, starting 4 processes with pool
            #below: for each color channel, list comprehension to set red values to white (value 255) & everything else to black (value 0)
            result = np.array(p.map(process_line, [(results[0][i], results[1][i], results[2][i]) for i in range(len(image))]))

    all_pixels = sum([len(result[i]) for i in range(len(result))])                                  # Getting total amount of pixels
    red_pixels = np.count_nonzero(result)                                                           # Finding total amount of red pixels by finding non-zero values 
    percentage = round(red_pixels * 100 / all_pixels, 2)                                            # Finding percentage of red pixels in the image  


    # If there are any white pixels in array, sum will be > 0
    red_detected = np.sum(result)                                                                   # Finding sum of result 
    data = (all_pixels, red_pixels, percentage)                                                     # Defining data variable
    if red_detected > 0 and percentage < 1:                                                         # If sum of matrix is over 0 and percentage of red pixels is over 1:
        #print('Potential fire detected!')
        return True, result, data                                                                   # Return boolean value True if sum is over 0
    else:   
        #print('No fire detected..')
        return False, result, data                                                                  # Else return boolean value False if sum is not over 0


if __name__ == "__main__":                                                                          # Defining main function
    from sys import argv                                                                                                          
    from os import chdir, path

    if len(argv) > 1:                           
        image = cv.imread(argv[1])
    else:
        chdir(path.dirname(argv[0]))                                                                # Change directory to script location
        image = cv.imread("../images/smallfire.jpg")                                                # Defaulting to test image
    hsl_pre = perf_counter()
    _, result, data = detect_fire(image, "hsl")
    hsl_post = perf_counter()
    
    rgb_pre = perf_counter()
    _, rgb, data = detect_fire(image, "rgb")
    rgb_post = perf_counter()

    rgb_pool_pre = perf_counter()
    _, pool, data = detect_fire(image, "pool_rgb")
    rgb_pool_post = perf_counter()

    print("Total amount of pixels in the image: " + str(data[0]))
    print("Amount of red pixels in the image: " + str(data[1]))  
    print("Percentage of red pixels: " + str(data[2]) + "%")
    print(f'hsl time:       {hsl_post-hsl_pre}')
    print(f'rgb time:       {rgb_post-rgb_pre}')
    print(f'rgb+pool time:  {rgb_pool_post-rgb_pool_pre}')
    for i in range(len(result)):
        for j in range(len(result[i])):
            assert rgb[i][j] == pool[i][j]                                                          # if true the algorithm is calculating correctly