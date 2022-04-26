from datetime import timezone
import datetime
import picamera
import picamera.array
import numpy as np

def capturePhoto():
    camera = picamera.PiCamera()
    camera.resolution =(2592,1944)
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    camera.capture('/home/pi/Desktop/%s.jpeg' % utc_timestamp)
    return '/home/pi/Desktop/%s.jpeg' % utc_timestamp

def captureRawData():
    with picamera.PiCamera() as camera:
        camera.resolution = (2592, 1944)
        image = np.empty((2600, 2000, 3), dtype=np.uint8)
        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        camera.capture(image, 'rgb')
        image = image[:2592, :1944]
        return image, utc_timestamp

if __name__ == "__main__":
    location = capturePhoto()
    print("Location: %" % location)
