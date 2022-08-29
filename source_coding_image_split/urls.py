from django.urls import path

from source_coding_image_split.views import RGB_split,YCbCr_split,downsample

app_name ='source_coding'
urlpatterns = [
    path('RGB/', RGB_split, name='RGB'),
    path('YCbCr/', YCbCr_split, name='YCbCr'),
    path('downsample/', downsample, name='downsample'),
]