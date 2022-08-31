
import cv2
from rest_framework.decorators import api_view
from rest_framework.response import Response

from source_coding_image_split.constants import IMAGE
from source_coding_image_split.utils import (
    change_intensity, convert_cv2_image_to_base64_URI, downsample_image,
    merge_RGB, merge_YCbCr, remove_n_least_significant_bits_from_pixels)


@api_view(['POST'])
def RGB_split(request):
    (B, G, R) = cv2.split(IMAGE)
    response = merge_RGB(R,G,B)
    if set(('b', 'g', 'r')).issubset(request.data):
        merge = cv2.merge([
                change_intensity(R, request.data['r']),
                change_intensity(G, request.data['g']),
                change_intensity(B, request.data['b'])
                ])
        response['Merge'] = merge
    return Response(response)


@api_view(['POST'])
def YCbCr_split(request):
    (Y, Cr, Cb) = cv2.split(cv2.cvtColor(IMAGE, cv2.COLOR_BGR2YCR_CB))
    response = merge_YCbCr(Y, Cb, Cr)
    if set(('y', 'cb', 'cr')).issubset(request.data):
        merge = cv2.cvtColor(
            cv2.merge([
                change_intensity(Y, request.data['y']),
                change_intensity(Cb, request.data['cb']),
                change_intensity(Cr, request.data['cr'])]),
            cv2.COLOR_YCrCb2BGR)
        response['Merge'] = merge
    return Response(response)


@api_view(['POST'])
def RGB_cutbits(request):
    (B, G, R) = cv2.split(IMAGE)
    if set(('b', 'g', 'r')).issubset(request.data):
        B = remove_n_least_significant_bits_from_pixels(B, request.data['b'])
        G = remove_n_least_significant_bits_from_pixels(G, request.data['g'])
        R = remove_n_least_significant_bits_from_pixels(R, request.data['r'])
    return Response(merge_RGB(R,G,B))

@api_view(['POST'])
def YCbCr_cutbits(request):
    (Y, Cr, Cb) = cv2.split(cv2.cvtColor(IMAGE, cv2.COLOR_BGR2YCR_CB))
    if set(('y', 'cb', 'cr')).issubset(request.data):
        Y = remove_n_least_significant_bits_from_pixels(Y, request.data['y'])
        Cb = remove_n_least_significant_bits_from_pixels(Cb, request.data['cb'])
        Cr = remove_n_least_significant_bits_from_pixels(Cr, request.data['cr'])
    return Response(merge_YCbCr(Y, Cb, Cr))


@api_view(['POST'])
def RGB_downsample(request):
    (B, G, R) = cv2.split(IMAGE)
    if set(('b', 'g', 'r')).issubset(request.data):
        B = downsample_image(B, request.data['b'])
        G = downsample_image(G, request.data['g'])
        R = downsample_image(R, request.data['r'])
    return Response(merge_RGB(R,G,B))


@api_view(['POST'])
def YCbCr_downsample(request):
    (Y, Cr, Cb) = cv2.split(cv2.cvtColor(IMAGE, cv2.COLOR_BGR2YCR_CB))
    if set(('y', 'cb', 'cr')).issubset(request.data):
        Y = downsample_image(Y, request.data['y'])
        Cb = downsample_image(Cb, request.data['cb'])
        Cr = downsample_image(Cr, request.data['cr'])
    return Response(merge_YCbCr(Y, Cb, Cr))
