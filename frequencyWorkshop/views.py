import string
import random
from datetime import datetime

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
import matplotlib.pyplot as plt
import librosa as librosa

from scipy.fftpack import fft, fftshift
import numpy as np
from scipy.io import wavfile

from .utils import *

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
    if duration == 0:
        duration = 0.001
    data, samplerate = librosa.load(file, offset=start, duration=duration, sr=None)

    N = len(data)
    T = 1.0 / samplerate
    yf = fft(data)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
    plt.xlabel("Frequency(Hz)")
    plt.xlim(0, 2000)
    plt.title("Frequency Domain")
    # plt.show()

    t = str(datetime.now().strftime('%H:%M-%S'))
    name = t + ''.join(random.choice(string.ascii_letters) for i in range(8))
    fft_dir = FFT_DIR + name + '.png'
    plt.savefig(FFT_DIR + name+'.png')
    plt.close(fig)

    return Response({'fft_dir': BASE_DIR + fft_dir})


@transaction.atomic
@api_view(['POST'])
def soundFilter(request):
    if 'sound_file' not in request.data:
        raise ParseError("Empty content")
    file_name = INPUT_SOUNDS_DIR + request.data['sound_file']

    if 'lowcut' in request.data:
        lowcut = float(request.data['lowcut'])
    else:
        lowcut = 50
    if 'highcut' in request.data:
        highcut = float(request.data['highcut'])
    else:
        highcut = 3000 #TODO change to the end of sound

    data, samplerate = librosa.load(file_name, sr=None)
    # data, rate = librosa.load(file_name, offset=start, duration=duration, sr=None)
    samples_num = len(data)

    filtered_data, data_filtered_f = ideal_bandpass_filter(data, samplerate, lowcut, highcut)
    # wavfile.write('Noisy_filtered.wav', fs, data_filtered.astype(np.float32))

    t = str(datetime.now().strftime('%H:%M-%S'))
    name = t + ''.join(random.choice(string.ascii_letters) for i in range(8))

    N = len(data)
    T = 1.0 / samplerate
    yf = fft(data)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
    plt.xlabel("Frequency(Hz)")
    # plt.xlim(0, 2000)
    plt.title("Frequency Domain (original sound)")
    if file_name == INPUT_SOUNDS_DIR + 'kotlet_kargah_2.wav':
        plt.ylim(0,0.02)

    if file_name == INPUT_SOUNDS_DIR + 'Noisy.wav':
        plt.ylim(0,0.3)
    fft_dir = FFT_DIR + 'fft' + name + '.png'
    plt.savefig(fft_dir)
    plt.close(fig)



    N = len(filtered_data)
    T = 1.0 / samplerate
    yf = data_filtered_f
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

    plt.clf()
    xff = np.linspace(-samplerate / 2, samplerate / 2, N)
    plt.plot(xff, 2.0 / N * abs(yf))
    plt.xlabel("Frequency(Hz)")
    plt.title("Frequency Domain (filtered sound)")
    if file_name == INPUT_SOUNDS_DIR + 'Noisy.wav':
        plt.ylim(0,0.3)
    plt.xlim(0, samplerate / 2)


    filtered_fft_dir = FFT_DIR + 'ffft' + name + '.png'
    plt.savefig(filtered_fft_dir)
    plt.close(fig)

    plt.clf()
    fig, ax = plt.subplots()
    x_range = [k / samplerate for k in range(0, samples_num)]
    ax.plot(x_range, filtered_data)
    plt.xlabel("Time(s)")
    plt.title("Time Domain (filtered sound)")
    if file_name == INPUT_SOUNDS_DIR + 'Noisy.wav':
        plt.xlim(0,0.03)
    time_dir = FFT_DIR + 'time' + name + '.png'
    plt.savefig(time_dir)
    plt.close(fig)


    sound_name = ''.join(random.choice(string.ascii_letters) for i in range(7))
    sound_dir = OUTPUT_SOUNDS_DIR + sound_name + '.mp3'
    wav.write(sound_dir, samplerate, filtered_data.astype(np.float32))

    return Response({'fft_dir': BASE_DIR + fft_dir,
                     'filtered_fft_dir': BASE_DIR + filtered_fft_dir,
                     'filtered_time_dir': BASE_DIR + time_dir,
                     'sound_dir': BASE_DIR + sound_dir})


@transaction.atomic
@api_view(['POST'])
def timeView(request):
    if 'sound_file' not in request.data:
        raise ParseError("Empty content")

    file = INPUT_SOUNDS_DIR + request.data['sound_file']

    data, rate = librosa.load(file, sr=None)
    samples_num = len(data)
    x_range = [k/rate for k in range(0, samples_num)]

    plt.clf()
    fig, ax = plt.subplots()
    ax.plot(x_range, data)
    plt.xlabel("Time(s)")
    plt.title("Time Domain")
    if file == INPUT_SOUNDS_DIR + 'Noisy.wav':
        plt.xlim(0, 0.03)

    t = str(datetime.now().strftime('%H:%M-%S'))
    name = t + ''.join(random.choice(string.ascii_letters) for i in range(8))
    time_dir = FFT_DIR + 'time' + name + '.png'
    plt.savefig(time_dir)
    plt.close(fig)

    N = len(data)
    T = 1.0 / rate
    yf = fft(data)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
    plt.xlabel("Frequency(Hz)")
    plt.title("Frequency Domain")
    if file == INPUT_SOUNDS_DIR + 'Noisy.wav':
        plt.ylim(0,0.3)
    if file == INPUT_SOUNDS_DIR + 'kotlet_kargah_2.wav':
        plt.ylim(0,0.02)
    fft_dir = FFT_DIR + 'fft' + name + '.png'
    plt.savefig(fft_dir)
    plt.close(fig)

    return Response({'time_dir': BASE_DIR + time_dir,
                     'fft_dir': BASE_DIR + fft_dir,
                     'f_domain': rate//2})
