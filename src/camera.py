from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution =(2592,1944)

#camera.start_preview()
for i in range(5):
    sleep(2)
    camera.capture('/home/pi/Desktop/testhalløj%s.jpeg' % i)
#camera.stop_preview()
