from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


from users.utils import send_code
from users.permissions import IsAdmin
from users.serializers import (
    UserSerializer,
    RegistrationSerializer,
    GetTokenSerializer
)

from reviews.constants import (
    ALLOW_METHODS,
    MESSAGE_NEW_CODE
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    Вьюсет для модели пользователей.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ALLOW_METHODS
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """
        Получить информацию о текущем пользователе.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def patch_me(self, request):
        """
        Обновить информацию о текущем пользователе.
        """
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationViewSet(CreateModelMixin, GenericViewSet):
    """
    Вьюсет для запроса на регистрацию пользователя.
    """

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Создает нового пользователя или
        отправляет код подтверждения существующему.
        """
        serializer = self.get_serializer(data=request.data)
        user = User.objects.filter(
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
    """
    Вьюсет для запроса на получение токена.
    """

    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Создает нового пользователя и выдает
        токен доступа на основе подтверждения кода.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
