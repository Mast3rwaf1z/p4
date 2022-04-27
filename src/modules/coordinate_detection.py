#from multiprocessing import Process
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
                    for _ in range(len(left_fire)):
                        upper_fire.append(left_fire.pop(0))
                    upper_fire.append((x,y))
                    if left_fire == []:
                        coords.pop(coords.index(left_fire))
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

    print(f'Number of fires:        {num_fires}')
    print(f'size of fires:          {sizes}')
    print(f'coordinate of fires:    {coordinates}')