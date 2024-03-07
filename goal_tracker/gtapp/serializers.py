from rest_framework import serializers
from .models import User, Pdp, Сompetence, Personal_goal, Personal_activity, Idea


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


# --- РАБОТА С ЛИЧНЫМИ ЦЕЛЯМИ ---

# Сериализатор для создания личных целей
class PersonalCreationSerializer(serializers.ModelSerializer):
    # Это чтобы при создании автоматически указывать пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        # Модель, которую будем использовать
        model = Personal_goal
        # Назначаем поля которые будем использовать
        fields = ['personal_goal_title', 'personal_goal_smart', 'expected_date_goal', 'user']

# Сериализатор для создания и редактирования действий, привязанных к личныя целям
class PersonalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую будем использовать
        model = Personal_activity
        # Назначаем поля которые будем использовать
        fields = ['personal_activity', 'regular_one_time', 'expected_date', 'done', 'personal_goal']


# Сериализатор для просмотра списка личных целей
class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal_goal
        fields = ('id', 'personal_goal_title', 'personal_goal_smart', 'expected_date_goal', 'done_goal',)
        # Идентификатор id нужен, чтобы потом можно было перейти из списка целей к просмотру одной цели по ее id.
        read_only_fields = ('id',)


# Сериализатор для просмотра и редактирования личной цели
class PersonalGoalSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую будем использовать
        model = Personal_goal
        # Назначаем поля которые будем использовать
        fields = ('id', 'personal_goal_title', 'personal_goal_smart', 'expected_date_goal', 'done_goal', 'personal_activities',)
        read_only_fields = ('id',)


# --- РАБОТА С ИПР И КАРЬЕРНЫМИ ЦЕЛЯМИ ---

# Сериализатор для создания и редактирования ИПР
class PdpSerializer(serializers.ModelSerializer):
    # Это чтобы при создании ИПР автоматически указывать пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        # Модель, которую будем использовать
        model = Pdp
        # Назначаем поля которые будем использовать
        fields = ['pdp_title', 'smart', 'expected_date', 'done', 'user']


# Сериализатор для создания и редактирования компетенций к добавления их к ИПР
class CompetenceSerializer(serializers.ModelSerializer):
    pdp = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Сompetence
        fields = ['competence', 'current_level', 'pdp', 'theory', 'theory_exp_date', 'theory_done', 'practice',
                  'practice_exp_date', 'practice_done']


# --- РАБОТА С ЗАМЕТКАМИ (ИДЕИ НА БУДУЩЕЕ) ---

# Сериализатор для заметок
class IdeaSerializer(serializers.ModelSerializer):
    # Это чтобы при создании автоматически указывать пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        # Модель, которую будем использовать
        model = Idea
        # Назначаем поля которые будем использовать
        fields = ['idea_title', 'description', 'user']

