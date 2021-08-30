from datetime import datetime

from django.shortcuts import render
import string
import random

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
import librosa as librosa

import numpy as np
import matplotlib.pyplot as plt
import cv2
import json


INPUT_IMAGE_DIR = 'media/imageWorkshop/input_images/'
OUTPUT_IMAGE_DIR = 'media/imageWorkshop/output_images/'
BASE_DIR = 'utility.rastaiha.ir/'

# Create your views here.
@transaction.atomic
@api_view(['POST'])
def threshold(request):
    if 'image_file' not in request.data:
        raise ParseError("Empty content")
    file_dir = INPUT_IMAGE_DIR + request.data['image_file']

    if 'threshold' not in request.data:
        raise ParseError("Empty content")
    tr = int(request.data['threshold'])

    im = cv2.imread(file_dir, 0)
    print(im[0])
    im[im < tr] = 0
    im[im >= tr] = 255
    print(im[0])

    t = str(datetime.now().strftime('%H:%M-%S'))
    name = t + ''.join(random.choice(string.ascii_letters) for i in range(8))
    image_dir = OUTPUT_IMAGE_DIR + name + '.png'
    plt.clf()
    fig = plt.figure()
    plt.imsave(arr=im, fname= image_dir, cmap='gray', vmin=0, vmax=255)
    plt.close(fig)
    return Response({'image_dir': BASE_DIR + image_dir})


@transaction.atomic
@api_view(['POST'])
def filter_im(request):
    if 'image_file' not in request.data:
        raise ParseError("Empty content")
    file_dir = INPUT_IMAGE_DIR + request.data['image_file']

    if 'kernel' not in request.data:
        raise ParseError("Empty content")
    # res = json.loads(stringA)
    if request.data['kernel'] == 'gaussian':
        im = cv2.imread(file_dir)
        filtered_im = cv2.GaussianBlur(im, (31, 31), 0)

    else:
        if type(request.data['kernel']) == list:
            kernel = np.array(request.data['kernel'])
        else:
            kernel = np.array(json.loads(request.data['kernel']))
        im = cv2.imread(file_dir)
        filtered_im = cv2.filter2D(im, -1, kernel)

    t = str(datetime.now().strftime('%H:%M-%S'))

    name = t + ''.join(random.choice(string.ascii_letters) for i in range(8))
    image_dir = OUTPUT_IMAGE_DIR + name + '.png'
    plt.clf()
    plt.figure(figsize=(20, 10))
    plt.imsave(arr=filtered_im, fname=image_dir)

    return Response({'image_dir': BASE_DIR + image_dir})


@transaction.atomic
@api_view(['POST'])
def channels(request):
    if 'image_file' not in request.data:
        file_dir = INPUT_IMAGE_DIR +'bar255.jpg'
    else:
        file_dir = INPUT_IMAGE_DIR + request.data['image_file']

    im = cv2.imread(file_dir)
    im = cv2.resize(im, (600, 400))

    # extract channels
    # G_channel = np.dstack((image[:, :, 1], image[:, :, 1], image[:, :, 1]))
    blue_channel = im[:, :, 0]
    green_channel = im[:, :, 1]
    red_channel = im[:, :, 2]

    t = str(datetime.now().strftime('%H:%M-%S'))
    name = t + ''.join(random.choice(string.ascii_letters) for i in range(8))
    blue_image_dir = OUTPUT_IMAGE_DIR+'blue' + name + '.png'
    red_image_dir = OUTPUT_IMAGE_DIR+'red' + name + '.png'
    green_image_dir = OUTPUT_IMAGE_DIR+'green' + name + '.png'

    # write channels to greyscale image
    plt.clf()
    plt.imsave(arr=blue_channel, fname=blue_image_dir, cmap='gray', vmin=0, vmax=255)
    plt.clf()
    plt.imsave(arr=green_channel, fname=green_image_dir, cmap='gray', vmin=0, vmax=255)
    plt.clf()
    plt.imsave(arr=red_channel, fname=red_image_dir, cmap='gray', vmin=0, vmax=255)

    return Response({'blue_image_dir': BASE_DIR + blue_image_dir,
                     'green_image_dir': BASE_DIR + green_image_dir,
                     'red_image_dir': BASE_DIR + red_image_dir})


@transaction.atomic
@api_view(['POST'])
def channels_mask(request):
    channels_code = {'G': 1, 'B': 0, 'R': 2}
    if 'image_file' not in request.data:
        file_dir = INPUT_IMAGE_DIR +'bar255.jpg'
    else:
        file_dir = INPUT_IMAGE_DIR + request.data['image_file']
    if 'color' not in request.data:
        color = 'G'
        c = channels_code[color]
    else:
        color = request.data['color']
        c = channels_code[color]
    if 'threshold' not in request.data:
        raise ParseError("Empty content")
    tr = int(request.data['threshold'])

    im = cv2.imread(file_dir)
    im = cv2.resize(im, (600, 400))
    channel = np.dstack((im[:, :, c], im[:, :, c], im[:, :, c]))
    ret, mask = cv2.threshold(channel, tr, 255, cv2.THRESH_BINARY)


    t = str(datetime.now().strftime('%H:%M-%S'))
    name = t + ''.join(random.choice(string.ascii_letters) for i in range(8))
    image_dir = OUTPUT_IMAGE_DIR + 'morpho2' + name + '.png'

    # write channels to greyscale image
    plt.clf()
    plt.imsave(arr=mask, fname=image_dir)
    plt.close()

    return Response({'image_dir': BASE_DIR + image_dir})


@transaction.atomic
@api_view(['POST'])
def dilate_erode(request):
    channels_code = {'G': 1, 'B': 0, 'R': 2}
    if 'image_file' not in request.data:
        file_dir = INPUT_IMAGE_DIR +'bar255.jpg'
    else:
        file_dir = INPUT_IMAGE_DIR + request.data['image_file']
    if 'color' not in request.data:
        color = 'G'
        c = channels_code[color]
    else:
        color = request.data['color']
        c = channels_code[color]
    if 'threshold' not in request.data:
        raise ParseError("Empty content")
    tr = int(request.data['threshold'])
    if 'method' not in request.data:
        raise ParseError("Empty content")
    method = request.data['method']
    if 'size' not in request.data:
        raise ParseError("Empty content")
    sizeSE = int(request.data['size'])

    im = cv2.imread(file_dir)
    im = cv2.resize(im, (600, 400))
    channel = np.dstack((im[:, :, c], im[:, :, c], im[:, :, c]))
    ret, mask = cv2.threshold(channel, tr, 255, cv2.THRESH_BINARY)

    SE = np.ones((sizeSE, sizeSE))
    if method == 'dilate':
        result = cv2.dilate(mask, SE)
    else:
        result = cv2.erode(mask, SE)

    t = str(datetime.now().strftime('%H:%M-%S'))
    name = t + ''.join(random.choice(string.ascii_letters) for i in range(8))
    image_dir = OUTPUT_IMAGE_DIR + name + '.png'

    # write channels to greyscale image
    plt.clf()
    plt.imsave(arr=result, fname=image_dir)

    return Response({'image_dir': BASE_DIR + image_dir})


@transaction.atomic
@api_view(['POST'])
def morpho_final(request):
    if 'image_file' not in request.data:
        file_dir = INPUT_IMAGE_DIR +'bar255.jpg'
    else:
        file_dir = INPUT_IMAGE_DIR + request.data['image_file']
    if 'mask_file' not in request.data:
        mask_dir = OUTPUT_IMAGE_DIR +'bar255.jpg'
    else:
        mask_dir = request.data['mask_file']
        mask_dir = mask_dir[mask_dir.find('media/'):]
    if 'method' not in request.data:
        raise ParseError("Empty content")
    method = request.data['method']
    if 'size' not in request.data:
        raise ParseError("Empty content")
    sizeSE = int(request.data['size'])

    image = cv2.imread(file_dir)
    image = cv2.resize(image, (600, 400))

    mask = cv2.imread(mask_dir)
    mask = cv2.resize(mask, (600, 400))

    SE = np.ones((sizeSE, sizeSE))
    if method == 'dilate':
        mainMask = cv2.dilate(mask, SE)
    else:
        mainMask = cv2.erode(mask, SE)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if mainMask[i, j, 1]:
                image[i, j, 1] = 255

    t = str(datetime.now().strftime('%H:%M-%S'))
    name = t + ''.join(random.choice(string.ascii_letters) for i in range(8))

    image_dir = OUTPUT_IMAGE_DIR + name + '.png'
    plt.clf()
    plt.imsave(arr=cv2.cvtColor(image, cv2.COLOR_BGR2RGB), fname=image_dir)
    
    plt.clf()
    mask_dir = OUTPUT_IMAGE_DIR + 'mask' + name + '.png'
    plt.imsave(arr=mainMask, fname=mask_dir)

    return Response({'image_dir': BASE_DIR + image_dir,
                     'mask_dir': BASE_DIR + mask_dir})
