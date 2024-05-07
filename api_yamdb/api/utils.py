from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail


def send_code(user):
    """
    Cоздает код для учетной записи пользователя и
    отправляет его на указанную электронную почту
    """
    code = default_token_generator.make_token(user)
    user.confirmation_code = code
    send_mail(
        subject='Подтверждение регистрации на YaMDB',
        message=f'Добрый день! Ваш код подтверждения: {code}',
        from_email=settings.EMAIL_FROM,
        recipient_list=[user.email]
    )
    user.save()
