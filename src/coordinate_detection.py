#from multiprocessing import Process
from cv2 import Mat, imread
import numpy as np

def get_channel(image:Mat, index:int) -> np.ndarray:
    return np.array([[values[index] for values in column] for column in image])

def get_coords(matrix:list[list[int]]) -> tuple[int, list[str], list[tuple], list[list[tuple]]]:
    #expect the given matrix is of data type list[list[int]]
    coords:list[list[tuple]] = list()
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] != 0:
                upper = matrix[y-1][x]
                left = matrix[y][x-1]
                upperleft = matrix[y-1][x-1]
                if upper == 0 and left == 0 and upperleft == 0:
                    coords.append([(x,y)])
                    matrix[y][x] = 100
                elif upper != 0 and left != 0:
                    for fire in coords:
                        if (x,y-1) in fire:
                            upper_fire = fire
                    for fire in coords:
                        if (x-1,y) in fire:
                            left_fire_index = coords.index(fire)
                            upper_fire_index = coords.index(upper_fire)
                            if left_fire_index == upper_fire_index:
                                coords[upper_fire_index].append((x,y))
                                break
                            for _ in range(len(fire)):
                                coords[upper_fire_index].append(coords[left_fire_index].pop(0))
                            coords[upper_fire_index].append((x,y))
                            if coords[left_fire_index] == []:
                                coords.pop(left_fire_index)

                elif upper != 0:
                    for fire in coords:
                        if (x,y-1) in fire:
                            fire.append((x,y))
                elif left != 0:
                    for fire in coords:
                        if (x-1,y) in fire:
                            fire.append((x,y))
                elif upperleft != 0:
                    for fire in coords:
                        if (x-1, y-1) in fire:
                            fire.append((x,y))

    
    return len(coords), [f'{len(fire)}px' for fire in coords], [coordinate[0] for coordinate in coords], coords



if __name__ == "__main__":
    from time import perf_counter
    from sys import argv
    pre = perf_counter()
    if len(argv) > 1:
        image = imread(argv[1])
    else:
        image = imread("smallfire.jpg")

    blue  = get_channel(image, 0)
    green = get_channel(image, 1)
    red   = get_channel(image, 2)
    matrix = [[255 if red[y][x] > 165 and green[y][x] < 100 and blue[y][x] < 100 else 0 for x in range(len(image[y]))] for y in range(len(image))]
    num_fires, sizes, coordinates, _ = get_coords(matrix)
    post = perf_counter()

    print(f'Number of fires:        {num_fires}')
    print(f'size of fires:          {sizes}')
    print(f'coordinate of fires:    {coordinates}')
    print(f'time:                   {post-pre}')