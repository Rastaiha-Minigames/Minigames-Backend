from django.urls import path

from imageWorkshop.views import *

app_name ='imageWorkshop'
urlpatterns = [
    path('threshold/', threshold, name='password'),
    path('filter/', filter_im, name='filter'),
    path('channels/', channels, name='channels'),
    path('morpho2/', channels_mask, name='morpho2'),
    path('morpho3/', dilate_erode, name='morpho3'),
    path('morpho4/', morpho_final, name='morpho4'),
]
