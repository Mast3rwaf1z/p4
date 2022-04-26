from picamera import PiCamera
from time import sleep
import time
import calender


camera = PiCamera()
camera.resolution =(2592,1944)

current_GMT = time.gmtime()
ts = calendar.timegm(current_GMT)
camera.capture('/home/pi/Desktop/{ts}.jpeg')
#camera.stop_preview()
