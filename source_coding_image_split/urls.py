from django.urls import path

import source_coding_image_split.views as views

app_name ='source_coding'
urlpatterns = [
    path('RGB_split/', views.RGB_split, name='RGB_split'),
    path('YCbCr_split/', views.YCbCr_split, name='YCbCr_split'),
    path('RGB_cutbits/', views.RGB_cutbits, name='RGB_cutbits'),
    path('YCbCr_cutbits/', views.YCbCr_cutbits, name='YCbCr_cutbits'),
    path('RGB_downsample/', views.RGB_downsample, name='RGB_downsample'),
    path('YCbCr_downsample/', views.YCbCr_downsample, name='YCbCr_downsample'),
]