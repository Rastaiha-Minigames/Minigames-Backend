from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person, Team
from .serializers import PersonSerializer,TeamSerializer

@api_view(["GET"])
def peopleList(request):
    people=Person.objects.all()
    teams=Team.objects.all().values_list('name',flat=True)
    serializedData=PersonSerializer(people,many=True,context={"request": request})
    return Response({'members':serializedData.data,'teams':teams})