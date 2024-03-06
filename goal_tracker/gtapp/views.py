from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from .models import User, Pdp, Personal_goal, Personal_activity, Idea, Сompetence
from .serializers import RegistrUserSerializer, PdpCreationSerializer, CompetenceCreationSerializer, \
    PersonalCreationSerializer, PersonalActivityCreationSerializer, PersonalSerializer, PersonalGoalSerializer, \
    IdeaSerializer

import xlwt


# --- ГЛАВНАЯ ---

# Главная страница с описанием проекта
class MainPage():
    def home(request):
        return render(request, 'home.html', {})


# --- РЕГИСТРАЦИЯ И ВХОД ---

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
        flag_idea = Idea.objects.filter(user=user_id).exists()

        # Создаю словарь с иформацией, которая передается в шаблон
        context = {'username': user.username, 'flag_pdp': flag_pdp, 'flag_personal': flag_personal,
                   'flag_idea': flag_idea}
        return render(request, 'profile/profile.html', context)


# --- РАБОТА С ЛИЧНЫМИ ЦЕЛЯМИ ---

# Представление для создания личных целей
class PersonalCreateView(APIView):
    def get(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        serializer = PersonalCreationSerializer()
        return Response(serializer.data)

    def post(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        # Получаю данные пользователя из сериалайзера
        serializer = PersonalCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.data)
        # Сохраняю цели
        serializer.save(user=self.request.user)
        return JsonResponse({'Status': True})


# Представление для того, чтобы добавлять действия к личным целям
class PersonalActivityCreateView(APIView):
    def get(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        serializer = PersonalActivityCreationSerializer()
        return Response(serializer.data)

    def post(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        # Получаю данные пользователя из сериалайзера
        serializer = PersonalActivityCreationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        # Сохраняю действие
        serializer.save()
        return JsonResponse({'Status': True})


# Представление для просмотра списка личных целей пользователя
class PersonalView(APIView):
    def get(self, request, username=None):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        queryset = Personal_goal.objects.filter(user=request.user.id)
        serializer = PersonalSerializer(queryset, many=True)
        return Response(serializer.data)


# Представление для просмотра, редактирования и удаления личной цели
class PersonalGoalView(RetrieveUpdateDestroyAPIView):
    queryset = Personal_goal.objects.all()
    serializer_class = PersonalGoalSerializer


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


# --- РАБОТА С ЗАМЕТКАМИ (ИДЕИ НА БУДУЩЕЕ) ---

# Представление для создания заметок
class IdeaCreateView(APIView):
    def get(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        serializer = IdeaSerializer()
        return Response(serializer.data)

    def post(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        # Получаю данные пользователя из сериалайзера
        serializer = IdeaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.data)
        # Сохраняю
        serializer.save(user=self.request.user)
        return JsonResponse({'Status': True})

# Представление для просмотра списка идей пользователя
class IdeaListView(ListAPIView):
    serializer_class = IdeaSerializer

    def get_queryset(self):
        return Idea.objects.filter(user=self.request.user)

# Представление для просмотра, редактирования и удаления заметки
class IdeaView(RetrieveUpdateDestroyAPIView):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer


# --- НАСТРОЙКА УВЕДОМЛЕНИЙ НА EMAIL ---
# В этом представлении пользователь может указать, хочет ли он получать уведомления на почту или будет ходить на сайт и
# отслеживать все события вручную.
class SettingsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'settings.html'

    def get(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)

        # Получаю id авторизованного пользователя
        user_id = request.user.id
        user = User.objects.get(pk=user_id)

        # Получаю информацию о том, включены ли уведомления на email в профиле пользователя
        flag_notifications = user.email_settings

        # Создаю словарь с иформацией, которая передается в шаблон
        context = {'username': user.username, 'email': user.email, 'flag_notifications': flag_notifications}
        return render(request, 'settings.html', context)

    def post(self, request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)

        # Получаю id авторизованного пользователя
        user_id = request.user.id
        user = User.objects.get(pk=user_id)

        # Получаю информацию о том, включены ли уведомления на email в профиле пользователя
        flag_notifications = user.email_settings

        # Если включены, то выключаю. Если выключены — включаю.
        if flag_notifications:
            user.email_settings = False
            user.save()
        else:
            user.email_settings = True
            user.save()

        # Направляю пользователя в профиль
        return redirect('profile')


# --- ВЫГРУЗКА ДАННЫХ ---
# Выгружает все данные пользователя в Excel-файл — карьерные цели, личные цели и заметки с идеями.
class DownloadView():
    def excel_create(request):
        # Закрываю страницу для неавторизованных пользователей
        if not request.user.is_authenticated:
            return HttpResponse(content='Вы не авторизованы. Войдите в систему.', status=403)

        # Создаю файл с ответом
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="goal_tracker.xls"'
        wb = xlwt.Workbook(encoding='utf-8')

        # Создаю таблицу ИПР
        if Pdp.objects.filter(user=request.user.id).exists():
            ws = wb.add_sheet('Personal Development Plan')

            # В первую строчку записываю название ИПР
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            pdp_column = Pdp.objects.filter(user=request.user.id).last().pdp_title
            ws.write(row_num, 0, pdp_column, font_style)

            # Во вторую строку записываю шапку
            row_num = 1
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ['Компетенция', 'Уровень', 'Обучение', 'Срок обучения', 'Статус обучения', 'Практика',
                       'Срок практики', 'Статус практики']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Заполняю таблицу ИПР
            font_style = xlwt.XFStyle()
            rows = Сompetence.objects.filter(pdp=Pdp.objects.filter(user=request.user.id).last()).values_list\
                ('competence', 'current_level', 'theory', 'theory_exp_date', 'theory_done', 'practice',
                 'practice_exp_date', 'practice_done')
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

        # Создаю таблицу с личными целями
        if Personal_goal.objects.filter(user=request.user.id).exists():
            ws = wb.add_sheet('Personal Goals')

            # В первую строчку записываю шапку
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ['Цель', 'Цель по SMART', 'Срок по цели', 'Статус цели', 'Действие', 'Характер', 'Срок для действия',
                       'Статус действия']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Заполняю таблицу с личными целями из двух связанных таблиц — Личные цели и Действия.
            font_style = xlwt.XFStyle()
            rows = Personal_goal.objects.filter(user=request.user.id).prefetch_related(
                'personal_activities__personal_activity',
                'personal_activities__regular_one_time',
                'personal_activities__expected_date',
                'personal_activities__done'
            ).values_list(
                'personal_goal_title',
                'personal_goal_smart',
                'expected_date_goal',
                'done_goal',
                'personal_activities__personal_activity',
                'personal_activities__regular_one_time',
                'personal_activities__expected_date',
                'personal_activities__done'
            )
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

        # Создаю таблицу для заметок с идеями
        if Idea.objects.filter(user=request.user.id).exists():
            ws = wb.add_sheet('Ideas')

            # В первую строчку записываю  шапку
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ['Заголовок', 'Описание']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Заполняю таблицу
            font_style = xlwt.XFStyle()
            rows = Idea.objects.filter(user=request.user.id).values_list('idea_title', 'description')
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response



