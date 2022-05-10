#this is main
from time import perf_counter
from cv2 import imread
from sys import argv

from modules.fire_detection import detect_fire, detect_fire_ir
from modules.coordinate_detection import get_coords

if len(argv) > 1:
    image = imread(argv[1])
    print(f'Analysing image:            {argv[1]}')
else:
    image = imread("images/smallfire.jpg")
    print(f'Analysing image:            {"images/firefirefire.jpg"}')
if len(argv) == 3:
    color_type = argv[2]
else:
    color_type = "rgb"

ir_image = imread("images/IRFire1.png")

print("Detecting fire...           ", end="")
pre_fire = perf_counter()
#state, processed_image, data = detect_fire(image, color_type)
state, processed_image, data = detect_fire_ir(image, ir_image)
post_fire = perf_counter()
print(f'{round(post_fire-pre_fire, 2)}s')
print(f'Amount of pixels:           {data[0]}')
print(f'Amount of red pixels:       {data[1]}')
print(f'Percentage of red pixels:   {data[2]}%')
if state:
    print(f'Potential fire detected')
    print("Getting coordinates...      ", end="")
    pre_coords = perf_counter()
    num_fires, sizes, coordinates, coords = get_coords(processed_image)
    post_coords = perf_counter()
    print(f'{round(post_coords-pre_coords, 2)}s')
    
    
    print(f'Number of fires:            {num_fires}')
    print(f'Sizes of fires:             {sizes}')
    print(f'coordinates of fires:       {coordinates}')
else:
    print(f'No fire detected')
