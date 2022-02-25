from django.urls import path
from .views import *

app_name ='choose_city'
urlpatterns = [
    path('choose/', choose, name='choose-city')
]