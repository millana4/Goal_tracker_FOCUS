from django.shortcuts import render
from .models import Pdp, User

# # функция для наполнения базы
# from django.http import HttpResponse
# import random
# def create_pdp(request):
#     anna = User.objects.get(email='tralfa81@gmail.com')
#     pdp = Pdp(pdp_title = random.choice(['получить грейд 1', 'получить грейд 2', 'получить грейд 3', 'получить грейд 4']),
#               smart = random.choice(['сделать к 13', 'сделать к 20', 'сделать к ноябрю']),
#               user = anna)
#     pdp.save()
#     return HttpResponse('DONE')
