#  Трекер целей FOCUS

##  О проекте
В приложении пользователь может собрать свои цели — профессиональные и личные, а также записывать идеи на будущее. Это помогает человеку сформулировать свои пожелания и держать их в фокусе. 

В приложении есть три типа целей:
- Индивидуальный план профессионального развития (ИПР).
- Личные желания.
- Идеи на будущее, которые нельзя реализовать прямо сейчас.

В приложении пользователь описывает свои планы. Затем приложение регулярно — еженедельно и ежемесячно отправляет пользователю письмо с напоминанием о его целях. Это помогает пользователю ничего не упускать и не забывать. 

*Прим. — Система рассылки пока не реализована.* 
##  Стек технологий
Технологии: **Django, DjangoRestFramework, PostgreSQL, Bootstrap, HTML.**

Работа с ИПР реализована на DjangoRestFramework с выводом в HTML. Фронтенд на Bootstrap.
Работа с личными целями и идеями реализована на DjangoRestFramework с выводом ответов в стиле API.
Есть выгрузка всех данных пользователя в Excel-файл. 


##  Схема сайта
![](https://github.com/millana4/Images/blob/main/Goal%20Tracker%20%D0%BD%D0%B0%20Django.jpg)

##  Схема базы данных
![](https://github.com/millana4/Images/blob/main/Database%20.jpg)

##  Как запустить проект
1. Скачайте проект Code → Download ZIP.
2. Запустите проект и создайте виртуальное окружение.
3. Установите зависимости из файла requirements.txt.
4. В папке проекта найдите файл .env.example. Откройте его и заполните настройки базы данных. Переименуйте файл в .env.
5. В терминале создайте базу данных:
`createdb -U postgres db_name`
6. Создайте миграции:
`python manage.py makemigrations`
7. Примените миграции:
`python manage.py migrate`
8. Запустите проект:
`python manage.py runserver`
