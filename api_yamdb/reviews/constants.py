GENRE_LENGTH = 256
SLUG_LENGTH = 50
TITLE_LENGTH = 256
SYMBOLS_LENGTH = 20

MIN_VALUE = 1
MAX_VALUE = 10

MESSAGE_MIN_VALUE = (f'Рейтинг ниже '
                     f'допустимого значения: {MIN_VALUE}')
MESSAGE_MAX_VALUE = (f'Рейтинг выше '
                     f'допустимого значения: {MAX_VALUE}')

PATH = 'static/data/'
UTF = 'UTF-8'
USERS = 'users.csv'
CATEGORY = 'category.csv'
GENRE = 'genre.csv'
TITLE = 'titles.csv'
GENRE_TITLE = 'genre_title.csv'
REVIEW = 'review.csv'
COMMENTS = 'comments.csv'

MESSAGE_DUPLICATE_REVIEW = ('Повторный отзыв на данное '
                            'произведение невозможен!')

ALLOW_METHODS = ('get', 'post', 'patch', 'delete')
MESSAGE_NEW_CODE = 'Новый код отправлен!'
MESSAGE_BAD_CODE = 'Неверный код подтверждения!'
