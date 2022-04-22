from cv2 import COLOR_BGR2GRAY, Mat, bitwise_and, cvtColor, imread, imshow, inRange, waitKey
import numpy as np



def get_channel(image:Mat, index:int) -> np.ndarray:
    return np.array([[values[index] for values in column] for column in image])

def get_coords(img:Mat) -> list[list[tuple]]:
    blue  = get_channel(img, 0)
    green = get_channel(img, 1)
    red   = get_channel(img, 2)
    grayscale = cvtColor(img, COLOR_BGR2GRAY)
    coords:list[list[tuple]] = list()
    for y in range(len(grayscale)):
        for x in range(len(grayscale[y])):
            grayscale[y][x] = 255 if red[y][x] > 165 and green[y][x] < 100 and blue[y][x] < 100 else 0
            if grayscale[y][x] != 0:
                upper = grayscale[y-1][x]
                left = grayscale[y][x-1]
                upperleft = grayscale[y-1][x-1]
                if upper == 0 and left == 0 and upperleft == 0:
                    coords.append([(x,y)])
                    grayscale[y][x] = 100
                elif upper != 0 and left != 0:
                    for fire in coords:
                        if (x,y-1) in fire:
                            upper_fire = fire
                        if (x-1,y) in fire:
                            left_fire_index = coords.index(fire)
                            upper_fire_index = coords.index(upper_fire)
                            if left_fire_index == upper_fire_index:
                                coords[upper_fire_index].append((x,y))
                                grayscale[y][x] = 100
                                break
                            for _ in range(len(fire)):
                                coords[upper_fire_index].append(coords[left_fire_index].pop(0))
                            coords[upper_fire_index].append((x,y))
                            grayscale[y][x] = 100
                            if coords[left_fire_index] == []:
                                coords.pop(left_fire_index)

                elif upper != 0:
                    for fire in coords:
                        if (x,y-1) in fire:
                            fire.append((x,y))
                            grayscale[y][x] = 100
                elif left != 0:
                    for fire in coords:
                        if (x-1,y) in fire:
                            fire.append((x,y))
                            grayscale[y][x] = 100
                elif upperleft != 0:
                    for fire in coords:
                        if (x-1, y-1) in fire:
                            fire.append((x,y))
                            grayscale[y][x] = 100
    
    print(f'Number of fires:        {len(coords)}')
    print(f'size of fires:          {[str(len(fire))+"px" for fire in coords]}')
    print(f'coordinate of fires:    {[coordinate[0] for coordinate in coords]}')
    #for coord in coords:
    #    print(coord)
    #imshow("img", grayscale)
    #waitKey()
    return coords



if __name__ == "__main__":
    from time import perf_counter
    from sys import argv
    pre = perf_counter()
    if len(argv) > 1:
        image = imread(argv[1])
    else:
        image = imread("smallfire.jpg")
    get_coords(image)
    post = perf_counter()
    print(post-pre)