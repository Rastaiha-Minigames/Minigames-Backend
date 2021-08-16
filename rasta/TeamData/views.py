from rest_framework.generics import ListAPIView
from .models import Person
from .serializers import PersonSerializer

class PeopleList(ListAPIView):
    queryset=Person.objects.all()
    serializer_class=PersonSerializer
