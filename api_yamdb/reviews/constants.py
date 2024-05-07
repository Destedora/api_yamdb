USERNAME_LENGTH = 150
EMAIL_LENGTH = 254
CODE_LENGTH = 254

SYMBOLS_LENGTH = 20
GENRE_LENGTH = 256
TITLE_LENGTH = 256
SLUG_LENGTH = 50

MAX_VALUE = 10
MIN_VALUE = 1

ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

ALLOW_METHODS = (
    'get',
    'post',
    'head',
    'options',
    'delete',
    'patch',
    'trace'
)

PATH = 'static/data/'
UTF = 'UTF-8'
USERS = 'users.csv'
CATEGORY = 'category.csv'
GENRE = 'genre.csv'
TITLE = 'titles.csv'
REVIEW = 'review.csv'
COMMENTS = 'comments.csv'

FORBIDDEN_USERNAME = 'me'
MESSAGE_USERNAME = (f'Регистрация пользователя с именем '
                    f'{FORBIDDEN_USERNAME} невозможна!')
MESSAGE_SYMBOLS = ('Пользователь с таким именем '
                   'содержит запрещенные символы!')

MESSAGE_MIN_VALUE = (f'Рейтинг ниже '
                     f'допустимого значения: {MIN_VALUE}')
MESSAGE_MAX_VALUE = (f'Рейтинг выше '
                     f'допустимого значения: {MAX_VALUE}')

MESSAGE_DUPLICATE_REVIEW = ('Повторный отзыв на данное '
                            'произведение невозможен!')
MESSAGE_DUPLICATE_USERNAME_EMAIL = ('Пользователь с таким именем '
                                    'или адресом электронной почты '
                                    'уже существует.')
MESSAGE_BAD_CODE = 'Неверный код подтверждения!'
