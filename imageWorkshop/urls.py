from django.urls import path

from imageWorkshop.views import threshold, channels, filter_im

app_name ='imageWorkshop'
urlpatterns = [
    path('threshold/', threshold, name='password'),
    path('filter/', filter_im, name='filter'),
    path('channels/', channels, name='channels'),
    # path('blending/', blending, name='blending'),
]
