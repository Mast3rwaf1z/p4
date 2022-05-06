import camera as cam
import cv2
from time import perf_counter

print("Capturing image...           ", end="")
time1 = perf_counter()
image, timestamp = captureRawData()
time2 = perf_counter()
print(f'{round(time2-time1, 2)}s')

print(image_data)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.imwrite("test.jpeg", image, [cv2.IMWRITE_JPEG_QUALITY, 95])
