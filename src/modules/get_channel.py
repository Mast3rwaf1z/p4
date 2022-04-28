from cv2 import Mat
from numpy import array, ndarray

def get_channel(image:Mat, index:int) -> ndarray:
    return array([[values[index] for values in row] for row in image])
