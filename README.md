# Проект YaMDb - агрегатор оценок и отзывов пользователей

## 💻 Cписок используемых технологий

[![pre-commit](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3111/) 
[![pre-commit](https://img.shields.io/badge/Django-3.2-092E20?logo=django&logoColor=white)](https://docs.djangoproject.com/en/4.2/releases/3.2/)
[![pre-commit](https://img.shields.io/badge/Django_REST_framework-3.12-800000?logo=djangorestramework&logoColor=white)](https://www.django-rest-framework.org/community/3.12-announcement/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)
[![PyJWT](https://img.shields.io/badge/PyJWT-2.1.0-000000?logo=python&logoColor=white)](https://github.com/jpadilla/pyjwt)
[![pytest](https://img.shields.io/badge/pytest-6.2.4-0A9EDC?logo=python&logoColor=white)](https://github.com/pytest-dev/pytest)
[![pytest-django](https://img.shields.io/badge/pytest_django-4.4.0-44B78B?logo=django&logoColor=white)](https://github.com/pytest-dev/pytest-django)
[![pytest-pythonpath](https://img.shields.io/badge/pytest_pythonpath-0.7.3-FF0000?logo=python&logoColor=white)](https://github.com/mverteuil/pytest-pythonpath)
[![Django REST Framework Simple JWT](https://img.shields.io/badge/Django_REST_Framework_Simple_JWT-5.3.0-0C4B33?logo=django&logoColor=white)](https://github.com/SimpleJWT/django-rest-framework-simplejwt)
[![django-filter](https://img.shields.io/badge/django_filter-23.3-0C4B33?logo=django&logoColor=white)](https://github.com/carltongibson/django-filter)


## 📝 Описание проекта

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## 🚀 Запуск проекта 

### Клонировать репозиторий:

```
git@github.com:Destedora/api_yamdb.git
```

### Cоздать виртуальное окружение:

```
python -m venv venv
```

### Активировать виртуальное окружение:


- Для Windows:
```
source venv/scripts/activate
```
- Для Linux/macOS:
```
source env/bin/activate
```

### Обновить менеджер пакетов pip:

```
python -m pip install --upgrade pip
```

### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
### Перейти в папку:

```
cd api_yamdb
```

### Выполнить миграции:

```
python manage.py migrate
```
###  Загрузка данных из CVS-файлов:

```
python manage.py csv_import
```

###  Запустить проект:

```
python manage.py runserver
```

### 🔸 Дополнительная документация проекта:

Полный перечень эндпоинтов: http://127.0.0.1:8000/redoc/

## ⌨️ Тестирование проекта
- При запущенном виртуальном окружении 
из корня проекта выполните комануду: 
```
pytest
```
- Подробная инструкция по работе с Postman-коллекцией 
для проверки API находится в файле `/postman_collection/README.md`.

## 🖱 Примеры запросов к API
- Регистрация пользователя:  
``` POST /api/v1/auth/signup/ ```  
- Получение данных своей учетной записи:  
``` GET /api/v1/users/me/ ```  
- Добавление новой категории:  
``` POST /api/v1/categories/ ```
- Удаление жанра:  
``` DELETE /api/v1/genres/{slug} ```
- Частичное обновление информации о произведении:  
``` PATCH /api/v1/titles/{titles_id} ```
- Получение списка всех отзывов:  
``` GET /api/v1/titles/{title_id}/reviews/ ```
- Добавление комментария к отзыву:  
``` POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/ ```

## 💾 Авторы

[![pre-commit](https://img.shields.io/badge/Дарья-Анохина-FFA500?logo=github&logoColor=white)](https://github.com/Destedora)
[![pre-commit](https://img.shields.io/badge/Роман-Абрамов-FFA500?logo=github&logoColor=white)](https://github.com/abramovrs)
[![pre-commit](https://img.shields.io/badge/Павел-Пушкарев-FFA500?logo=github&logoColor=white)](https://github.com/PushkarevP)
