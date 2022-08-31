import numpy
import cv2

IMAGE = cv2.imread('media/cat.jpg')
ZERO_MATRIX = numpy.zeros(IMAGE.shape[:2], dtype="uint8")
HALF_MATRIX = numpy.array([[127]*IMAGE.shape[1]] *
                          IMAGE.shape[0]).astype(IMAGE.dtype)
