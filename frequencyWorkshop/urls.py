from django.urls import path

from frequencyWorkshop.views import soundFilter, fftView, timeView

app_name='TeamData'
urlpatterns = [
    path('fft/', fftView, name='fft'),
    path('timeplot/', timeView, name='fft'),
    path('filter/', soundFilter, name='filter')
]
