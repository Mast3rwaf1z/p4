from picamera import PiCamera
from datetime import timezone
import datetime

def capturePhoto():
    camera = PiCamera()
    camera.resolution =(2592,1944)
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    camera.capture('/home/pi/Desktop/%s.jpeg' % utc_timestamp)
    return '/home/pi/Desktop/%s.jpeg' % utc_timestamp

if __name__ == "__main__":
    string = capturePhoto()
    print(string)
