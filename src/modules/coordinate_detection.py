#from multiprocessing import Process
from multiprocessing import Pool


try:
    from modules.get_channel import get_channel
except:
    from get_channel import get_channel

def get_fire(coords, coordinate): #get the list of pixels contained in the fire at a certain index
    for fire in coords:
        if coordinate in fire:
            return fire

def check_line(matrix:list[list[int]], coords:list[list[tuple[int]]], y:int):
    for x in range(len(matrix[y])):
        if matrix[y][x] != 0:
            if x == 0 and y == 0:
                coords.append([(x,y)])
                continue
            upper = matrix[y-1][x]
            left = matrix[y][x-1]
            upperleft = matrix[y-1][x-1]
            if upper == 0 and left == 0 and upperleft == 0:
                coords.append([(x,y)])
            elif upper != 0 and left != 0:
                upper_fire = get_fire(coords, (x, y-1))
                left_fire = get_fire(coords, (x-1, y))
                if left_fire == upper_fire:
                    upper_fire.append((x,y))
                else:
                    upper_fire.extend(left_fire)
                    coords.remove(left_fire)
                    upper_fire.append((x,y))
            elif upper != 0:
                get_fire(coords, (x, y-1)).append((x,y))
            elif left != 0:
                get_fire(coords, (x-1, y)).append((x,y))
            elif upperleft != 0:
                get_fire(coords, (x-1, y-1)).append((x,y))
    return coords

def get_coords(matrix:list[list[int]]) -> tuple[int, list[str], list[tuple], list[list[tuple]]]:
    #expect the given matrix is of data type list[list[int]]
    coords:list[list[tuple[int]]] = list()
    for y in range(len(matrix)):
        coords = check_line(matrix, coords, y)
    
    return len(coords), [f'{len(fire)}px' for fire in coords], [coordinate[0] for coordinate in coords], coords

def compare_lines(data):
    line1, line2, index = data
    coords = list()
    for i in range(len(line2)):
        if line2[i] != 0:
            if line2[i-1] != 0 and line1[i] != 0:
                left_fire = get_fire(coords, (i-1, index))
                left_fire.append((i,index))
                left_fire.append((i, index-1))
            elif line2[i-1] != 0:
                get_fire(coords, (i-1, index)).append((i, index))
            elif line1[i] != 0:
                coords.append([(i, index)])
                coords[coords.index([(i, index)])].append((i, index-1))
            else:
                coords.append([(i, index)])
    return coords


def get_coords_pool(matrix:list[list[int]]) -> tuple[int, list[str], list[tuple], list[list[tuple]]]:
    coords = list()
    with Pool(4) as p: #time step 1
        coords = p.map(compare_lines, [(matrix[i], matrix[i-1], i) for i in range(len(matrix))])
        print([x for x in coords if x])

if __name__ == "__main__":
    from cv2 import imread
    from sys import argv
    from os import chdir, path
    chdir(path.dirname(argv[0])) #change directory to script location
    
    if len(argv) > 1:
        image = imread(argv[1])
    else:
        image = imread("../images/smallfire.jpg")

    blue  = get_channel(image, 0)
    green = get_channel(image, 1)
    red   = get_channel(image, 2)
    matrix = [[255 if red[y][x] > 165 and green[y][x] < 100 and blue[y][x] < 100 else 0 for x in range(len(image[y]))] for y in range(len(image))]
    num_fires, sizes, coordinates, _ = get_coords(matrix)

    #get_coords_pool(matrix)

    print(f'Number of fires:        {num_fires}')
    print(f'size of fires:          {sizes}')
    print(f'coordinate of fires:    {coordinates}')