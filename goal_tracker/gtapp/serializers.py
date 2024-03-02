from rest_framework import serializers
from .models import User, Pdp, Сompetence


# Сериализатор для регистрации пользователя
class RegistrUserSerializer(serializers.ModelSerializer):
    # Поле для повторения пароля
    password2 = serializers.CharField()

    # Настройка полей
    class Meta:
        # Модель, которую будем использовать
        model = User
        # Назначаем поля которые будем использовать
        fields = ['email', 'username', 'password', 'password2']

    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = User(
            email=self.validated_data['email'],  # Назначаем Email
            username=self.validated_data['username'],  # Назначаем Логин
        )
        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя 
        return user


# --- РАБОТА С ИПР И КАРЬЕРНЫМИ ЦЕЛЯМИ ---
# Сериализатор для создания ИПР
class PdpCreationSerializer(serializers.ModelSerializer):
    # Это чтобы при создании ИПР автоматически указывать пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        # Модель, которую будем использовать
        model = Pdp
        # Назначаем поля которые будем использовать
        fields = ['pdp_title', 'smart', 'expected_date', 'user']


# Сериализатор для создания компетенций к добавления их к ИПР
class CompetenceCreationSerializer(serializers.ModelSerializer):
    pdp = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Сompetence
        fields = ['competence', 'current_level', 'pdp', 'theory', 'theory_exp_date', 'practice', 'practice_exp_date']
