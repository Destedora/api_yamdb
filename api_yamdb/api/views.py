from http import HTTPStatus
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (IsAdminIsModeratorIsAuthor,
                          IsAdminIsUserOrReadOnly,
                          IsSuperUserOrIsAdmin)
from .serializers import (CustomUserSerializer,
                          CreateUserSerializer,
                          TokenSerializer)
from .utils import send_confirmation_code
from users.models import CustomUser


User = get_user_model()


class APISignUp(APIView):
    """Создание нового пользователя."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = CustomUser.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).first()
        if user:
            confirmation_code = default_token_generator.make_token(user)
            send_confirmation_code(email=user.email,
                                   confirmation_code=confirmation_code)
            return Response('Новый код отправлен', status=status.HTTP_200_OK)
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(email=user.email,
                               confirmation_code=confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIToken(APIView):
    """Получение токена."""

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(CustomUser, username=request.data['username'])
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Неверный код подтверждения'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        if User.objects.filter(username=username, email=email).exists():
            send_confirmation_code(username, email)
            return Response(request.data, status=status.HTTP_200_OK)
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code(username, email)
        return Response(serializer.data, status=HTTPStatus.OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsSuperUserOrIsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(permissions.IsAuthenticated,),
        url_name='me',
        url_path='me'
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
