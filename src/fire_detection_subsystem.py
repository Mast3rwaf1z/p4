#this is main
from cv2 import imread
from sys import argv

from modules.fire_detection import detect_fire
from modules.coordinate_detection import get_coords

if len(argv) > 1:
    image = imread(argv[1])
    print(f'Analysing image:            {argv[1]}')
else:
    image = imread("images/smallfire.jpg")
    print(f'Analysing image:            {"images/smallfire.jpg"}')
if len(argv) == 3:
    color_type = argv[2]
else:
    color_type = "rgb"

state, processed_image, data = detect_fire(image, color_type)

num_fires, sizes, coordinates, coords = get_coords(processed_image)

if state:
    print(f'Potential fire detected')
else:
    print(f'No fire detected')
print(f'Amount of pixels:           {data[0]}')
print(f'Amount of red pixels:       {data[1]}')
print(f'Percentage of red pixels:   {data[2]}')
print(f'Number of fires:            {num_fires}')
print(f'Sizes of fires:             {sizes}')
print(f'coordinates of fires:       {coordinates}')
