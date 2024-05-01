from rest_framework import routers
from django.urls import include, path
from .views import (
    APIToken,
    UserViewSet,
    UserCreateView
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', APIToken.as_view()),
    path('v1/auth/signup/', UserCreateView.as_view())
]
