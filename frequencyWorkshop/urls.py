from django.urls import path

from frequencyWorkshop.views import soundFilter, fftView

app_name='TeamData'
urlpatterns = [
    path('fft/', fftView, name='fft'),
    path('filter/', soundFilter, name='filter')
]
