from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from .models import User, Pdp, Personal_goal, Financial_goal, Idea, Сompetence
from .serializers import RegistrUserSerializer, PdpCreationSerializer, CompetenceCreationSerializer


# Главная страница с описанием проекта
class MainPage():
    def home(request):
        return render(request, 'home.html', {})


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


# Стартовая страница профиля, откуда можно все формы можно создавать и просматривать
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
        context = {'username': user.username, 'flag_pdp': flag_pdp, 'flag_personal': flag_personal,
                   'flag_finance': flag_finance, 'flag_idea': flag_idea, }
        return render(request, 'profile/profile.html', context)


# --- РАБОТА С ИПР И КАРЬЕРНЫМИ ЦЕЛЯМИ ---
# Представление для создания ИПР
class PdpCreateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile/pdp_creation.html'

    def get(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)
        serializer = PdpCreationSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)
        # Получаю данные пользователя из сериалайзера
        serializer = PdpCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        # Сохраняю pdp
        serializer.save(user=self.request.user)
        return redirect('competence')


# Представление для того, чтобы добавлять необходимые комепетенции в ИПР
class CompetenceCreateView(CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile/competence.html'

    def get(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)
        serializer = CompetenceCreationSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)
        # Получаю данные пользователя из сериалайзера
        serializer = CompetenceCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        # Сохраняю компетенцию и указываю что она относится к последнему ИПР пользователя
        serializer.save(pdp=Pdp.objects.filter(user=request.user.id).last())
        return redirect('competence')


# Представление для просмотра ИПР
class PdpView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile/pdp.html'

    def get(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)
        queryset = Сompetence.objects.filter(pdp=Pdp.objects.filter(user=request.user.id).last())
        return Response({'serializer': queryset})


# Предупреждение об удалении ИПР
class PdpDeleteView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile/pdp_attention.html'

    def get(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)
        message = 'Вы уверены, что хотите удалить ИПР?'
        return Response({'message': message})

    # Метод Delete не сработал, пробовала, поэтому использую Post
    def post(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)
        # Удаляю последний ИПР пользователя
        Pdp.objects.filter(user=request.user.id).last().delete()
        return redirect('profile')
