from django.urls import path
from .views import PeopleList
app_name='TeamData'
urlpatterns = [
    path('people/',PeopleList.as_view(),name='PeopleList')
]
