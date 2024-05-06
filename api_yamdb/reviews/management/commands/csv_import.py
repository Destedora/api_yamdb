import csv

from django.core.management.base import (
    BaseCommand,
    CommandError
)


from users.models import User

from reviews.costants import (
    PATH,
    UTF,
    USERS,
    CATEGORY,
    GENRE,
    TITLE,
    REVIEW,
    COMMENTS
)
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)


class Command(BaseCommand):
    help = ('Загрузка данных из CSV-файлов в базу данных:'
            'python manage.py csv_import')

    @staticmethod
    def import_users():
        """Импорт пользователей из CSV-файла в базу данных"""
        with open(f'{PATH}{USERS}', 'r', encoding=UTF) as file_csv:
            objs = [
                User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
                for row in csv.DictReader(file_csv)
            ]
            User.objects.bulk_create(objs)

    @staticmethod
    def import_category():
        """Импорт категорий из CSV-файла в базу данных"""
        with open(f'{PATH}{CATEGORY}', 'r', encoding=UTF) as file_csv:
            objs = [
                Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                for row in csv.DictReader(file_csv)
            ]
            Category.objects.bulk_create(objs)

    @staticmethod
    def import_genre():
        """Импорт жанров из CSV-файла в базу данных"""
        with open(f'{PATH}{GENRE}', 'r', encoding=UTF) as file_csv:
            objs = [
                Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                for row in csv.DictReader(file_csv)
            ]
            Genre.objects.bulk_create(objs)

    @staticmethod
    def import_titles():
        """Импорт произведений из CSV-файла в базу данных"""
        with open(f'{PATH}{TITLE}', 'r', encoding=UTF) as file_csv:
            objs = [
                Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )
                for row in csv.DictReader(file_csv)
            ]
            Title.objects.bulk_create(objs)

    @staticmethod
    def import_review():
        """Импорт отзывов из CSV-файла в базу данных"""
        with open(f'{PATH}{REVIEW}', 'r', encoding=UTF) as file_csv:
            objs = [
                Review(
                    id=row['id'],
                    text=row['text'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                    author_id=row['author'],
                    title_id=row['title_id'],
                )
                for row in csv.DictReader(file_csv)
            ]
            Review.objects.bulk_create(objs)

    @staticmethod
    def import_comments():
        """Импорт комментариев из CSV-файла в базу данных"""
        with open(f'{PATH}{COMMENTS}', 'r', encoding=UTF) as file_csv:
            objs = [
                Comment(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date'],
                )
                for row in csv.DictReader(file_csv)
            ]
            Comment.objects.bulk_create(objs)

    def handle(self, *args, **options):
        """Импорт данных из нескольких CSV-файлов в базу данных"""
        try:
            self.import_users()
            self.import_category()
            self.import_genre()
            self.import_titles()
            self.import_review()
            self.import_comments()
        except Exception as error:
            raise CommandError(f'Невозможно открыть файл: {error}')
        self.stdout.write(
            self.style.SUCCESS('Данные из CSV-файла были успешно '
                               'импортированы в базу данных!')
        )
