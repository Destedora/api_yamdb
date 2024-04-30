USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)
USERNAME_LENGTH = 150
EMAIL_LENGTH = 254
CODE_LENGTH = 254


FORBIDDEN_USERNAME = 'me'
MESSAGE_USERNAME = (f'Регистрация пользователя с именем '
                    f'{FORBIDDEN_USERNAME} невозможна!')
MESSAGE_SYMBOLS = ('Пользователь с именем "{username}" '
                   'содержит запрещенные символы:\n{symbols}')
