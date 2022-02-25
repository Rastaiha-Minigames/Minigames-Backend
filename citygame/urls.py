from django.urls import path
from .views import *

app_name ='choose_city'
urlpatterns = [
    path('choose/', choose, name='choose-city'),
    path('reset/', reset_game, name='reset-game'),
    path('result/', result_game, name='result-game'),
    path('people/', people_answer, name='people-answers')
]