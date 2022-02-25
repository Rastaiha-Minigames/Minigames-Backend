from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

city_score = {
    "Rome":3000,
    "Milan":2000,
    "Napel":1500,
    "Turin":1200,
    "Palermo":900,
    "Genova":700,
    "Bulunia":600,
    "Venize":300
}
phone_answer = dict()

def counter(city_name):
    city_ctr = 0
    for p, c in phone_answer.items():
        if c == city_name:
            city_ctr += 1
    return city_ctr

@api_view(['POST'])
def choose(request):
    phone_number = request.data['phone_number']
    city = request.data['city']

    if phone_number in phone_answer:
        choosed_city = phone_answer[phone_number]
        return Response(data={'message':f'شما قبلا شرکت کرده بودید و امتیاز شما برابر است با {city_score[choosed_city] / counter(choosed_city)}'})
    
    phone_answer[phone_number] = city
    
    return Response(data={'message':f'انتخاب شما ثبت شد و امتیاز شما برابر است با {city_score[city] / counter(city)}'})
