import string
import random

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
import matplotlib.pyplot as plt
import librosa as librosa

from scipy.fftpack import fft
import numpy as np

INPUT_SOUNDS_DIR = 'media/frequencyWorkshop/input_sounds/'
OUTPUT_SOUNDS_DIR = 'media/frequencyWorkshop/output_sounds/'
FFT_DIR = 'media/frequencyWorkshop/FFT/'
BASE_DIR = 'utility.rastaiha.ir/'


@transaction.atomic
@api_view(['POST'])
def fftView(request):
    if 'sound_file' not in request.data:
        raise ParseError("Empty content")
    if 'start' in request.data:
        start = float(request.data['start'])
    else:
        start = 0.0
    if 'end' in request.data:
        duration = float(request.data['end'])-start
    else:
        duration = None

    file = INPUT_SOUNDS_DIR + request.data['sound_file']
    print(file)

    data, rate = librosa.load(file, offset=start, duration=duration)
    samples_num = len(data)

    print(samples_num)

    fft_out = fft(data)

    x_range = [k * rate / samples_num for k in range(0, (samples_num // 2))]
    plt.plot(x_range, np.abs(fft_out[-1*(samples_num // 2):]))

    name = ''.join(random.choice(string.ascii_letters) for i in range(6))
    fft_dir = FFT_DIR + name + '.png'
    plt.savefig(FFT_DIR + name+'.png')

    # f = open('media/' + name+'.png', 'w')
    # plot_file = File(f)
    # output = FFTFiles.objects.create(fft_file=plot_file)
    return Response({'fft_dir': BASE_DIR + fft_dir})



@transaction.atomic
@api_view(['POST'])
def soundFilter(request):
    if 'sound_file' not in request.data:
        raise ParseError("Empty content")
    file_name = request.data['sound_file']

    if 'lowcut' in request.data:
        lowcut = float(request.data['lowcut'])
    else:
        lowcut = 0.0
    if 'highcut' in request.data:
        highcut = float(request.data['highcut'])
    else:
        highcut = 10 #TODO change to the end of sound

    return Response({'success': True}, status=status.HTTP_200_OK)

