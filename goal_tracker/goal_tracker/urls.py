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
    PdpDeleteView

# from gtapp.views import create_pdp

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', MainPage.home, name='home'),
                  path('accounts/', include('django.contrib.auth.urls')),

                  path('registration/', RegistrUserView.as_view(), name='registration'),
                  path('profile/', ProfileView.look_profile, name='profile'),
                  path('pdp_creation/', PdpCreateView.as_view(), name='pdp_creation'),
                  path('competence/', CompetenceCreateView.as_view(), name='competence'),
                  path('pdp/', PdpView.as_view(), name='pdp'),
                  path('pdp_attention/', PdpDeleteView.as_view(), name='pdp_attention'),

                  path('api-auth', include('rest_framework.urls')),
                  path('auth/', include('djoser.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# path('new_pdp/', create_pdp),          # функция для наполнения базы
