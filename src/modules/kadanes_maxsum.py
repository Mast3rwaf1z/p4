import numpy as np
import cv2
import timeit

# reading the image
image = cv2.imread("firefirefire.jpg")
image1 = image.copy()
#cv2.imshow('image',image1)

# Setting a resolution to resize image for faster processing of Kadanes algorithm. Doesn't work without it...
res = 150
image = cv2.resize(image, (res, res),interpolation = cv2.INTER_NEAREST)

# Grayscaling image
gray1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray1 = gray1.astype(np.int16)  # we need negative values for Kadanes algorithm, so converting to int16 that has the range of numbers -32768 to +32767.

#printing array and shape of matrix
print("Gray-scaled array is \n",gray1)
print("\n Shape is ",gray1.shape) 


def kadanes_algorithm(array, start, finish, n):
    Sum = 0
    maxSum = -9999
    finish[0] = -1
    local_start = 0
 
    for i in range(n):
        Sum += array[i]
        if Sum < 0:
            Sum = 0
            local_start = i + 1
        elif Sum > maxSum:
            maxSum = Sum
            start[0] = local_start
            finish[0] = i

    if finish[0] != -1:
        return maxSum

    maxSum = array[0]
    start[0] = finish[0] = 0

    for i in range(1, n):
        if array[i] > maxSum:
            maxSum = array[i]
            start[0] = finish[0] = i
    return maxSum

def find_max_sum(M):
    global Rightrow ,Rightcol, Leftcol , Leftrow ,  ROW, COL,LeftRight,TopBottom
    maxSum  = -9999
    global finalLeft , finalRight , finalTop , finalBottom , left , right 
    i = 0 
 
    temp = [None] * ROW
    Sum = 0
    start = [0]
    finish = [0]

    for left in range(COL):
        temp = [0] * ROW
        for right in range(left, COL):
            for i in range(ROW):
                temp[i] += M[i][right]
            Sum = kadanes_algorithm(temp, start, finish, ROW)
            if Sum > maxSum:
                maxSum = Sum
                finalLeft = left
                finalRight = right
                finalTop = start[0]
                finalBottom = finish[0]

    Leftrow = finalTop
    Leftcol = finalLeft    
    print("(Top, Left)", "(", finalTop,finalLeft, ")")
    Rightrow = finalRight
    Rightcol = finalBottom
    print("(Bottom, Right)", "(", finalBottom,finalRight, ")")
    print("Max sum is:", maxSum)

    print("leftrow",Leftrow)
    print(finalLeft)
    


if __name__ == "__main__":

    ROW = gray1.shape[0]
    COL = gray1.shape[1]
    start = timeit.default_timer()
    find_max_sum(gray1)
    stop = timeit.default_timer()
    print('Time: ', stop - start) 

    # getting the coordinates of centre of circle.
    TopBottom = int((finalBottom + finalTop)/2)
    LeftRight = int((finalLeft + finalRight)/2)
    print("Centre of circle is: ",LeftRight,TopBottom)

    # getting the original image to which we want to reapply the ratio.
    grayimg = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

    # applying ratio to get the image properly with exact coordinates of bright area in main image.
    LeftRight = int(grayimg.shape[1]/(res/LeftRight))
    TopBottom = int(grayimg.shape[0]/(res/TopBottom))

    # Displaying the image with circled bright area.    
    cv2.circle(image1, (LeftRight,TopBottom), 100, (255, 0, 0), 2)
    cv2.imshow("Kadane", image1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()