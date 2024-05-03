from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.permissions import IsAdminOrSuperuser
from users.serializers import (
    UserSerializer,
    RegistrationSerializer,
    GetTokenSerializer
)
from users.utils import send_code
from users.models import CustomUser

from reviews.constants import (
    ALLOW_METHODS,
    MESSAGE_NEW_CODE,
    MESSAGE_BAD_CODE
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    """Вьюсет для модели Пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ALLOW_METHODS
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        url_path='me',
        url_name='me',
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """
        Получает информацию о текущем пользователе
        или обновляет ее в случае метода PATCH
        """
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RegistrationViewSet(CreateModelMixin, GenericViewSet):
    """Вьюсет для запроса на регистрацию пользователя."""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Создает нового пользователя или
        отправляет код подтверждения существующему
        """
        serializer = self.get_serializer(data=request.data)
        user = CustomUser.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).first()
        if user:
            send_code(user)
            return Response(
                MESSAGE_NEW_CODE,
                status=status.HTTP_200_OK
            )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class GetTokenViewSet(CreateModelMixin, GenericViewSet):
    """Вьюсет для запроса на получение Токена"""

    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Создает нового пользователя и выдает
        токен доступа на основе подтверждения кода
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED)
        return Response(
            MESSAGE_BAD_CODE,
            status=status.HTTP_400_BAD_REQUEST
        )
