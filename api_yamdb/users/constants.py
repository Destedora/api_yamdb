ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

USERNAME_LENGTH = 150
EMAIL_LENGTH = 254
CODE_LENGTH = 254


FORBIDDEN_USERNAME = 'me'
MESSAGE_USERNAME = (f'Регистрация пользователя с именем '
                    f'{FORBIDDEN_USERNAME} невозможна!')
MESSAGE_SYMBOLS = ('Пользователь с таким именем '
                   'содержит запрещенные символы!')

MESSAGE_DUPLICATE_USERNAME = ('Данное имя пользователя '
                              'уже используется')
MESSAGE_DUPLICATE_EMAIL = ('Данный адрес электронной '
                           'почты уже зарегистрирован')
