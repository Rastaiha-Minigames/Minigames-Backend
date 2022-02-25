from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

KEY = 'zoorkhooneh'

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

@api_view(['POST'])
def reset_game(request):
    recv_key = request.data['key']
    if recv_key == KEY:
        phone_answer.clear()
        return Response(data={'message':'داده ها با موفقیت پاک شدند'})
    
    return Response(data={'message':'کد وارد کرده اشتباه است'})

@api_view(['POST'])
def result_game(request):
    recv_key = request.data['key']
    if recv_key == KEY:
        scores = dict()
        for c, s in city_score.items():
            attends = counter(c)
            if attends == 0:
                scores[c] = 0
            else:
                scores[c] = s / attends

        return Response(data=scores)

    return Response(data={'message':'کد وارد کرده اشتباه است'})

@api_view(['POST'])
def people_answer(request):
    recv_key = request.data['key']
    if recv_key == KEY:
        return Response(data=phone_answer)
    
    return Response(data={'message':'کد وارد کرده اشتباه است'})