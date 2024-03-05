from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User, PermissionsMixin


# Создаю класс менеджера пользователей
class CustomUserManager(BaseUserManager):

    # Метод для создания обычного пользователя
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Вы не ввели email')
        if not username:
            raise ValueError('Вы не ввели имя')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Метод для создания админа
    def create_superuser(self, email, username, password=None, **extra_fields):
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


# Модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=254, unique=True)
    username = models.CharField(verbose_name='Имя', max_length=50, default='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True)
    email_settings = models.BooleanField(verbose_name='Настройка уведомлений', default=True)
    is_admin = models.BooleanField(verbose_name='Админ', default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # уникальный идентификатор пользователя
    REQUIRED_FIELDS = ['username']  # поля для создания суперпользователя

    objects = CustomUserManager()  # Добавляю методы класса CustomUserManager

    class Meta:
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'Пользователи'

    def __str__(self):
        return self.email


# Модель ИПР (индивидуальный план развития). Здесь задается цель, ее подробное описание по технологии SMART,
# срок, в который пользователь планирует достичь цель, а также отметка о достижении цели.
class Pdp(models.Model):
    objects = models.manager.Manager()
    pdp_title = models.CharField(verbose_name='Карьерная цель', max_length=100)
    smart = models.CharField(verbose_name='Карьерная цель по SMART', max_length=700, null=True, blank=True)
    expected_date = models.DateField(verbose_name='Срок', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='pdps')
    created_at = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(verbose_name='Статус', default=False)

    class Meta:
        verbose_name = 'ИПР'
        verbose_name_plural = 'ИПР'
        db_table = 'ИПР'

    def __str__(self):
        return f'{self.pdp_title}'


# Описываются компетенции, которые нужно развить, чтобы достичь карьерной цели.
class Сompetence(models.Model):
    LEVEL_CHOICES = {
        'Не владею': 'Не владею',
        'Есть представление': 'Есть представление',
        'Есть небольшой опыт': 'Есть небольшой опыт',
        'Немного владею': 'Немного владею',
        'Неплохо владею': 'Неплохо владею',
        'Полностью владею': 'Полностью владею',
    }

    objects = models.manager.Manager()
    competence = models.CharField(verbose_name='Компетенция', max_length=200)
    current_level = models.CharField(verbose_name='Уровень владения', choices=LEVEL_CHOICES, null=True, blank=True)
    pdp = models.ForeignKey(Pdp, on_delete=models.CASCADE, verbose_name='ИПР', related_name='сompetencies')
    theory = models.CharField(verbose_name='Обучение', max_length=200, null=True, blank=True)
    theory_exp_date = models.DateField(verbose_name='Срок', blank=True, null=True)
    theory_done = models.BooleanField(verbose_name='Статус', default=False)
    practice = models.CharField(verbose_name='Практика', max_length=200, null=True, blank=True)
    practice_exp_date = models.DateField(verbose_name='Срок', blank=True, null=True)
    practice_done = models.BooleanField(verbose_name='Статус', default=False)

    class Meta:
        verbose_name = 'Компетенция'
        verbose_name_plural = 'Компетенции'
        db_table = 'Компетенции'

    def __str__(self):
        return f'{self.competence}'


# Модель для личной цели: название, подробное описание по технологии SMART, срок и отметка о выполнеии
class Personal_goal(models.Model):
    objects = models.manager.Manager()
    personal_goal_title = models.CharField(verbose_name='Личная цель', max_length=300)
    personal_goal_smart = models.CharField(verbose_name='Личная цель по SMART', max_length=700, null=True, blank=True)
    expected_date = models.DateField(verbose_name='Срок', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='personal_goal')
    created_at = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(verbose_name='Статус', default=False)

    class Meta:
        verbose_name = 'Личная цель'
        verbose_name_plural = 'Личные цели'
        db_table = 'Личные цели'

    def __str__(self):
        return f'{self.personal_goal_title}'


# Модель действий, которые необходимо совершить, чтобы достичь какой-то цели.
# Действие может быть регулярным, например, ходить в бассейн дважды в неделю, и может быть разовым — сходить к врачу.
class Personal_activity(models.Model):
    REGULAR_CHOICES = {
        'regular': 'Регулярное действие',
        'one time': 'Разовое действие',
    }

    objects = models.manager.Manager()
    personal_activity = models.CharField(verbose_name='Действие', max_length=200)
    regular_one_time = models.CharField(verbose_name='Регулярное / разовое', choices=REGULAR_CHOICES, null=True,
                                        blank=True)
    expected_date = models.DateField(verbose_name='Срок', blank=True, null=True)
    done = models.BooleanField(verbose_name='Статус', default=False)
    personal_goal = models.ForeignKey(Personal_goal, on_delete=models.CASCADE, verbose_name='Цель',
                                      related_name='personal_activities')

    class Meta:
        ordering = ('expected_date',)
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'
        db_table = 'Действия'

    def __str__(self):
        return f'{self.personal_activity}'


# Модель для заметок, в которых можно записывать идеи на долгий срок.
class Idea(models.Model):
    objects = models.manager.Manager()
    idea_title = models.CharField(verbose_name='Заголовок', max_length=100)
    description = models.CharField(verbose_name='Описание', max_length=5000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='ideas')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Идея'
        verbose_name_plural = 'Идеи на будущее'
        db_table = 'Идеи'

    def __str__(self):
        return f'{self.idea_title}'
