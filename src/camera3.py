import time
import picamera
import picamera.array
import numpy as np

with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1952)
    time.sleep(2)
    image = np.empty((2600, 2000, 3), dtype=np.uint8)
    camera.capture(image, 'rgb')
    image = image[:2592, :1952]
