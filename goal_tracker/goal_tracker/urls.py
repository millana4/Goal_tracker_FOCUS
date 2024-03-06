"""
URL configuration for goal_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from gtapp.views import MainPage, RegistrUserView, ProfileView, PdpCreateView, CompetenceCreateView, PdpView, \
    PdpDeleteView, PersonalCreateView, PersonalActivityCreateView, PersonalView, PersonalGoalView, IdeaCreateView, \
    IdeaListView, IdeaView, SettingsView, DownloadView, CheckProgressView, CompetenceUpdateView, PdpUpdateView, \
    PersonalActivityUpdateView

# from gtapp.views import create_pdp

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', MainPage.home, name='home'),
                  path('accounts/', include('django.contrib.auth.urls')),

                  path('registration/', RegistrUserView.as_view(), name='registration'),
                  path('profile/', ProfileView.look_profile, name='profile'),
                  path('pdp_creation/', PdpCreateView.as_view(), name='pdp_creation'),
                  path('competence/', CompetenceCreateView.as_view(), name='competence'),
                  path('competence_update/<int:pk>/', CompetenceUpdateView.as_view(), name='competence_update'),
                  path('pdp/', PdpView.as_view(), name='pdp'),
                  path('pdp_update/<int:pk>/', PdpUpdateView.as_view(), name='pdp_update'),
                  path('pdp_attention/', PdpDeleteView.as_view(), name='pdp_attention'),
                  path('personal_creation/', PersonalCreateView.as_view(), name='personal_creation'),
                  path('personal_action/', PersonalActivityCreateView.as_view(), name='personal_action'),
                  path('personal_action/<int:pk>/', PersonalActivityUpdateView.as_view(), name='personal_action_update'),
                  path('personal_list/', PersonalView.as_view(), name='personal'),
                  path('personal_goal/<int:pk>/', PersonalGoalView.as_view(), name='personal_goal'),
                  path('idea_creation/', IdeaCreateView.as_view(), name='idea_creation'),
                  path('idea_list/', IdeaListView.as_view(), name='idea_list'),
                  path('idea/<int:pk>/', IdeaView.as_view(), name='idea'),

                  path('settings/', SettingsView.as_view(), name='settings'),
                  path('download/', DownloadView.excel_create, name='download'),
                  path('check_progress/', CheckProgressView.as_view(), name='check_progress'),

                  path('api-auth', include('rest_framework.urls')),
                  path('auth/', include('djoser.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# path('new_pdp/', create_pdp),          # функция для наполнения базы
