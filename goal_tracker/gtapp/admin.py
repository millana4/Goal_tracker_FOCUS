from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Pdp, Personal_goal, Financial_goal, Idea
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Форма создания пользователя. Прописываем, так как стандартная модель пользователя была изменена.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "username",]

    def clean_password2(self):
        # Проверка, что пароль введенный второй раз сопадает с первым
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароль не совпадает")
        return password2

    def save(self, commit=True):
        # Хеширование и сохранение пароля
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Форма изменения пользователя. Нужна, так как стандартная модель была изменена.
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "username", "password", "is_admin"]

# Создаю классы инлайнов, чтобы связанные с пользователем таблицы (ИПР, личные и финансовые цели, идеи)
# можно было посмотреть и отредактировать в карточке пользователя.
class PdpInstanceInline(admin.TabularInline):
     model = Pdp
     extra = 1


class Personal_goalInstanceInline(admin.TabularInline):
    model = Personal_goal
    extra = 1


class Financial_goalInstanceInline(admin.TabularInline):
    model = Financial_goal
    extra = 1


class IdeaInstanceInline(admin.StackedInline):
    model = Idea
    extra = 1

class UserAdmin(BaseUserAdmin):
    # Включаем формы для удаления и изменения пользователя
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "username", "id", "is_admin"]   # поля, которые нужно показывать в таблице пользователей
    list_filter = ["is_admin"]                               # фильтр справа

    # настройка полей с информацией о пользователе
    fieldsets = [
        (None, {"fields": ["email", "username"]}),
        ("Разрешения", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = [
        (None,{"classes": ["wide"],
                "fields": ["email", "password1", "password2"],
               },
         ),
    ]
    search_fields = ["email"]         # по какому полю искать
    ordering = ["email"]              # по какому полю соритровать

    # для просмотра связанных с пользователем таблиц
    inlines = [PdpInstanceInline, Personal_goalInstanceInline, Financial_goalInstanceInline, IdeaInstanceInline]

    filter_horizontal = []


# Регистрация модели пользователя
admin.site.register(User, UserAdmin)





# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)

# class PdpInstanceInline(admin.TabularInline):
#     model = Pdp
#
# class UserAdmin(BaseUserAdmin):
#     list_display = ['email', 'id', 'username', 'is_admin']
#     list_filter = ('is_admin',)
#     search_fields = ["email"]
#     ordering = ["email"]
#
#
#
#     inlines = [PdpInstanceInline]
#
#
# admin.site.register(User, UserAdmin)
# admin.site.register(Pdp)

# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/
# это как в админке настраивать пользователькие модели юзеров
