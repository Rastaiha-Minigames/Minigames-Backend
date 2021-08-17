from rest_framework.serializers import ModelSerializer,StringRelatedField,SerializerMethodField
from .models import Person, Team

class TeamSerializer(ModelSerializer):
    class Meta:
        model=Team
        fields=('name',)
class PersonSerializer(ModelSerializer):

    team=StringRelatedField(many=True)
    picture = SerializerMethodField()
    class Meta:
        model = Person
        fields=('name','team','description','position','picture')

    def get_picture(self, person):
        request = self.context.get('request')
        picture_url = person.picture.url
        return request.build_absolute_uri(picture_url)