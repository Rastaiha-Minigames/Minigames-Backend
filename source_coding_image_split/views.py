import base64

import cv2
import numpy
from rest_framework.decorators import api_view
from rest_framework.response import Response

image = cv2.imread('media/cat.jpg')

def image_to_base64(image):
    _, buffer = cv2.imencode(".jpg", image)
    string = base64.b64encode(buffer).decode()
    return f"data:image/jpg;base64,{string}"


@api_view(['POST'])
def RGB_split(request):
    zeros = numpy.zeros(image.shape[:2], dtype="uint8")
    (B, G, R) = cv2.split(image)
    try:
        blue_coefficient = request.data['b']
        green_coefficient = request.data['g']
        red_coefficient = request.data['r']
    except:
        blue_coefficient = 1
        green_coefficient = 1
        red_coefficient = 1
    merge = cv2.merge([(B*blue_coefficient).astype('uint8'),
                      (G*green_coefficient).astype('uint8'), (R*red_coefficient).astype('uint8')])
    B = cv2.merge([B, zeros, zeros])
    G = cv2.merge([zeros, G, zeros])
    R = cv2.merge([zeros, zeros, R])
    return Response({
        'B': image_to_base64(B),
        'G': image_to_base64(G),
        'R': image_to_base64(R),
        'Merge': image_to_base64(merge),
    })


@api_view(['POST'])
def YCbCr_split(request):
    (Y, Cr, Cb) = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB))
    half = numpy.array([[127]*Y.shape[1]]*Y.shape[0]).astype(Y.dtype)
    try:
        Y_coefficient = request.data['y']
        Cr_coefficient = request.data['cr']
        Cb_coefficient = request.data['cb']
    except:
        Y_coefficient = 1
        Cr_coefficient = 1
        Cb_coefficient = 1
    merge = cv2.cvtColor(cv2.merge([(Y*Y_coefficient).astype(Y.dtype), (Cr*Cr_coefficient).astype(
        Y.dtype), (Cb*Cb_coefficient).astype(Y.dtype)]), cv2.COLOR_YCrCb2BGR)
    Y = cv2.cvtColor(cv2.merge([Y, half, half]), cv2.COLOR_YCrCb2BGR)
    Cr = cv2.cvtColor(cv2.merge([half, Cr, half]), cv2.COLOR_YCrCb2BGR)
    Cb = cv2.cvtColor(cv2.merge([half, half, Cb]), cv2.COLOR_YCrCb2BGR)
    return Response({
        'Y': image_to_base64(Y),
        'Cb': image_to_base64(Cb),
        'Cr': image_to_base64(Cr),
        'Merge': image_to_base64(merge),
    })


@api_view(['POST'])
def downsample(request):
    try:
        scale_factor = request.data['factor']
    except:
        scale_factor = 1
    original_dim = (image.shape[1], image.shape[0])
    dim = (int(image.shape[1]*scale_factor), int(image.shape[0]*scale_factor))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_LANCZOS4)
    img = cv2.resize(resized, original_dim)
    return Response({
        'image': image_to_base64(img),
    })
