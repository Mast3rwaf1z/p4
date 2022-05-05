#testing with raw data capture
from cv2 import imread, imwrite
from sys import argv
from time import perf_counter
from modules.fire_detection import detect_fire
from modules.coordinate_detection import get_coords
from modules.camera import capturePhoto, captureRawData
from modules.client import send

print("Capturing image...           ", end="")
time1 = perf_counter()
image, timestamp = captureRawData()
time2 = perf_counter()
print(f'{round(time2-time1, 2)}s')

print('Analysing image...')

if len(argv) == 2:
    color_type = argv[1]
else:
    color_type = "rgb"

print("Detecting fire...           ", end="")
pre_fire = perf_counter()
state, processed_image, data = detect_fire(image, color_type)
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

print("Sending image...           ", end="")

imwrite(f"{timestamp}.jpeg", image)
time1 = perf_counter()
send(f"{timestamp}.jpeg")
time2 = perf_counter()
print(f'{round(time2-time1, 2)}s')
