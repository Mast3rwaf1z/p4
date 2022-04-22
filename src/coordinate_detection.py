from cv2 import COLOR_BGR2GRAY, Mat, bitwise_and, cvtColor, imread, imshow, inRange, waitKey
import numpy as np



def get_channel(image:Mat, index:int) -> np.ndarray:
    return np.array([[values[index] for values in column] for column in image])

def get_coords(img:Mat):
    blue  = get_channel(img, 0)
    green = get_channel(img, 1)
    red   = get_channel(img, 2)
    grayscale = cvtColor(img, COLOR_BGR2GRAY)
    index = 0
    indices = [[0 for j in range(len(grayscale[i]))] for i in range(len(grayscale))]
    for y in range(len(grayscale)):
        for x in range(len(grayscale[y])):
            grayscale[y][x] = 255 if red[y][x] > 165 and green[y][x] < 100 and blue[y][x] < 100 else 0
            if grayscale[y][x] != 0:
                upper = grayscale[y-1][x]
                left = grayscale[y][x-1]
                if upper == 0 and left == 0:
                    index += 1
                    indices[y][x] = index
                elif upper != 0 and left != 0:
                    if indices[y-1][x] > indices[y][x-1]:
                        indices[y-1][x] = indices[y][x-1]
                        index -= 1
                    elif indices[y][x-1] > indices[y-1][x]:
                        indices[y][x-1] = indices[y-1][x]
                        index -= 1
    for slice1 in indices:
        for slice2 in slice1:
            if slice2 != 0:
                print(slice2)
                
    print(index)




if __name__ == "__main__":
    from time import perf_counter
    pre = perf_counter()
    image = imread("smallfire.jpg")
    print(get_coords(image))
    post = perf_counter()
    print(post-pre)