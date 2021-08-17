from django.urls import path
from .views import peopleList
app_name='TeamData'
urlpatterns = [
    path('people/',peopleList,name='PeopleList')
]
