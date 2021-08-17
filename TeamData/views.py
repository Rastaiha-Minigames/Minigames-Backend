from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Person
from .serializers import PersonSerializer

@api_view(["GET"])
def peopleList(request):
    people=Person.objects.all()
    serializedData=PersonSerializer(people,many=True)
    return Response({'members':serializedData.data})