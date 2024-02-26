from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Pdp, User
from .serializers import RegistrUserSerializer

# Главная страница с описанием проекта
class MainPage():
    def home(request):
        return render(request,'home.html', {})

class RegistrUserView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration/registration.html'

    # Метод для загрузки полей регистрации
    def get(self, request):
        serializer = RegistrUserSerializer()
        return Response({'serializer': serializer})

    # Метод для регистрации пользователя
    def post(self, request):
        # Получаю данные пользователя из сериалайзера
        serializer = RegistrUserSerializer(data=request.data)
        # Проверяю корректность данных
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        # Сохраняю нового пользователя
        serializer.save()

        # Авторизую нового пользователя
        username = serializer.data['email']
        password = serializer.data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        # Напревляю в личный кабинет
        return redirect('profile')

















# # Можно так сделать регистрацию — ответ в стиле API, а не HTML
# class RegistrUserView(CreateAPIView):
#     # Добавляем в queryset
#     queryset = User.objects.all()
#     # Добавляем serializer RegistrUserSerializer
#     serializer_class = RegistrUserSerializer
#     # Добавляем права доступа
#     permission_classes = [AllowAny]
#
#     # Создаём метод для создания нового пользователя
#     def post(self, request, *args, **kwargs):
#         # Добавляем UserRegistrSerializer
#         serializer = RegistrUserSerializer(data=request.data)
#         # Создаём список data
#         data = {}
#         # Проверка данных на валидность
#         if serializer.is_valid():
#             # Сохраняем нового пользователя
#             serializer.save()
#             # Добавляем в список значение ответа True
#             data['response'] = True
#             # Возвращаем что всё в порядке
#             return Response(data, status=status.HTTP_200_OK)
#         else:  # Иначе
#             # Присваиваем data ошибку
#             data = serializer.errors
#             # Возвращаем ошибку
#             return Response(data)
#
## А это та же самая страница регистрации, но с использованием форм и без DRF
# from .forms import UserRegistrationForm
# class RegistrUserView():
#     def registr(request):
#         if request.method == 'POST':
#             user_form = UserRegistrationForm(request.POST)
#             if user_form.is_valid():
#                 # Create a new user object but avoid saving it yet
#                 new_user = user_form.save(commit=False)
#                 # Set the chosen password
#                 new_user.set_password(user_form.cleaned_data['password'])
#                 # Save the User object
#                 new_user.save()
#                 return render(request, 'registration/registr_done.html', {'new_user': new_user})
#         else:
#             user_form = UserRegistrationForm()
#         return render(request, 'registration/registration.html', {'user_form': user_form})


# Чтобы писать вью-классы для зарегистрированных пользователей
# from django.contrib.auth.mixins import LoginRequiredMixin


# ТУТ НАПИСАНО КАК АВТОРИЗОВАТЬ ПОСЛЕ РЕГИСТРАЦИИ
# def register_user(request):
#
#     # Если метод запроса POST
#     if request.method == 'POST':
#
#         # Берем данные с формы проверяем их
#         # если все в порядке сохраняем нового пользователя
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#             # Авторизуем пользователя и переходим на главную страницу
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('dashboard')
#
#         # Если что-то пошло не так отображаем форму
#         # с данными которые ввел пользователь для
#         # их исправления
#         context = {'form': form}
#         return render(request, 'app/register.html', context)
#
#     # При GET запросе отображаем пустую форму
#     context = {'form': UserCreationForm()}
#     return render(request, 'app/register.html', context)











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