from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from .models import User, Pdp, Personal_goal, Financial_goal, Idea
from .serializers import RegistrUserSerializer

# Главная страница с описанием проекта
class MainPage():
    def home(request):
        return render(request,'home.html', {})


# Регистрация пользователя
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
        # Направляю в личный кабинет
        return redirect('profile')


class ProfileView():
    def look_profile(request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)

        # Получаю id авторизованного пользователя
        user_id = request.user.id
        user = User.objects.get(pk=user_id)

        # Получаю информацию о том, заполнены или цели
        flag_pdp = Pdp.objects.filter(user=user_id).exists()
        flag_personal = Personal_goal.objects.filter(user=user_id).exists()
        flag_finance = Financial_goal.objects.filter(user=user_id).exists()
        flag_idea = Idea.objects.filter(user=user_id).exists()

        # Создаю словарь с иформацией, которая передается в шаблон
        context = {'username': user.username,'flag_pdp': flag_pdp, 'flag_personal': flag_personal,'flag_finance': flag_finance,'flag_idea': flag_idea,}
        return render(request, 'profile.html', context)


