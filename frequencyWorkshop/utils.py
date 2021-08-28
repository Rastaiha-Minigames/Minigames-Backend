import librosa as librosa
from scipy.io import wavfile as wav
from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

#
# def run():
#     import numpy as np
#     import matplotlib.pyplot as plt
#     from scipy.signal import freqz
#     fname = '../media/frequencyWorkshop/input_sounds/kotlet_kargah.wav'
#     outname = '../media/frequencyWorkshop/output_sounds/filtered.wav'
#
#     # Sample rate and desired cutoff frequencies (in Hz).
#     fs = 6000.0
#     lowcut = 50.0
#     highcut = 1000.0
#
#     # Plot the frequency response for a few different orders.
#     plt.figure(1)
#     plt.clf()
#     for order in [3, 6, 9]:
#         b, a = butter_bandpass(lowcut, highcut, fs, order=order)
#         w, h = freqz(b, a, worN=2000)
#         plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)
#
#     plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
#              '--', label='sqrt(0.5)')
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Gain')
#     plt.grid(True)
#     plt.legend(loc='best')
#
#     # Filter a noisy signal.
#     T = 0.05
#     nsamples = int(T * fs)
#     t = np.linspace(0, T, nsamples, endpoint=False)
#     a = 0.02
#     f0 = 600.0
#     x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
#     x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
#     x += a * np.cos(2 * np.pi * f0 * t + .11)
#     x += 0.03 * np.cos(2 * np.pi * 2000 * t)
#     plt.figure(2)
#     plt.clf()
#     plt.plot( x, label='Noisy signal')
#     # print(t)
#     # print(x)
#
#     y = butter_bandpass_filter(x, lowcut, highcut, fs, order=9)
#     # print(y)
#     print(len(y))
#     plt.plot( y, label='Filtered signal (%g Hz)' % f0)
#     plt.xlabel('time (seconds)')
#     plt.hlines([-a, a], 0, T, linestyles='--')
#     plt.grid(True)
#     plt.axis('tight')
#     plt.legend(loc='upper left')
#
#     plt.show()
#     # librosa.write_wav(outname, y, rate)
#     # wav.write(outname, rate, y)


# run()
#
# import matplotlib.pyplot as plt
# import numpy as np
# import wave
# import sys
# import math
# import contextlib
#
# fname = '../media/frequencyWorkshop/input_sounds/kotlet_kargah.wav'
# outname = '../media/frequencyWorkshop/output_sounds/filtered.wav'
#
# cutOffFrequency = 400.0
#
#
# # from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
# def running_mean(x, windowSize):
#   cumsum = np.cumsum(np.insert(x, 0, 0))
#   return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize
#
#
# # from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
# def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):
#
#     if sample_width == 1:
#         dtype = np.uint8 # unsigned char
#     elif sample_width == 2:
#         dtype = np.int16 # signed 2-byte short
#     else:
#         raise ValueError("Only supports 8 and 16 bit audio formats.")
#
#     channels = np.fromstring(raw_bytes, dtype=dtype)
#
#     if interleaved:
#         # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
#         channels.shape = (n_frames, n_channels)
#         channels = channels.T
#     else:
#         # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
#         channels.shape = (n_channels, n_frames)
#
#     return channels
#
#
# with contextlib.closing(wave.open(fname,'rb')) as spf:
#     sampleRate = spf.getframerate()
#     ampWidth = spf.getsampwidth()
#     nChannels = spf.getnchannels()
#     nFrames = spf.getnframes()
#
#     # Extract Raw Audio from multi-channel Wav File
#     signal = spf.readframes(nFrames*nChannels)
#     spf.close()
#     channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)
#
#     # get window size
#     # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
#     freqRatio = (cutOffFrequency/sampleRate)
#     N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)
#
#     # Use moviung average (only on first channel)
#     filtered = running_mean(channels[0], N).astype(channels.dtype)
#
#     wav_file = wave.open(outname, "w")
#     wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
#     wav_file.writeframes(filtered.tobytes('C'))
#     wav_file.close()


# import matplotlib.pyplot as plt
# from scipy.io import wavfile as wav
# from scipy.fftpack import fft
# import numpy as np
#
# data, rate = librosa.load('static/RZFWLXE-bell-hop-bell.mp3')
#
# samples_num = len(data)
# print(data.shape)
# print(rate)
# print(len(data)/rate)
# fft_out = fft(data)
# x_range = [k*rate/samples_num for k in range(0, (samples_num//2))]
# print(len(x_range))
# # print(x_range)
# plt.plot(x_range , np.abs(fft_out[len(data)//2:]))
# plt.savefig('./test.png')