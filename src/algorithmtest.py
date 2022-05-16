#this is main
from time import perf_counter
from cv2 import imread
from sys import argv

from modules.fire_detection import detect_fire
from modules.coordinate_detection import get_coords

color_type = "pool_rgb"
fires = [0 for i in range(53)]
actual_fires = [0 for i in range(53)]
fireno = 0
for x in range(53):
    if x < 46 and x > 0:
        if x % 3 == 0:
            actual_fires[x] = 1
            fireno += 1
fn = 0
fp = 0
tn = 0
tp = 0

def tester(path):
    image = imread(path)
    print(f'Analysing image:            {path}')
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
        return True
    else:
        print(f'No fire detected')
        return False

for i in range(1, 53):
    print(f'Test {i} running now')
    y = tester(f"modules/fires/{i}.png")
    if(y):
        fires[i] = 1

for x in range(1, 53):
    if actual_fires[x] == fires[x]:
        if actual_fires[x] == 1:
            tp += 1
        else:
            tn += 1
    if actual_fires[x] > fires[x]:
        fn += 1
    if fires[x] > actual_fires[x]:
        fp += 1

print(f'True Positive: {tp}')
print(f'False Positive: {fp}')
print(f'True Negative: {tn}')
print(f'False Negative: {fn}')
print(f'Accuracy: {((tp+tn)/(tp+fp+tn+fn))*100}')
