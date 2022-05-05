from datetime import timezone
import datetime
import picamera
import picamera.array
import numpy as np

def capturePhoto(resolution = (2592, 1944)):
    camera = picamera.PiCamera()
    camera.resolution = resolution
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    location = '/home/pi/Desktop/%s.jpeg' % utc_timestamp
    camera.capture(location)
    return location

def captureRawData(resolution = (2592, 1944)):
    with picamera.PiCamera() as camera:
        camera.resolution = resolution
        image = np.empty((2600, 2000, 3), dtype=np.uint8)
        dt = datetime.datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        camera.capture(image, 'rgb')
        image = image[:resolution[1], :resolution[2]]
        return image, utc_timestamp

if __name__ == "__main__":
    location = capturePhoto()
    print("Location: %s" % location)
