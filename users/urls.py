from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet
from . import views


v1_router = DefaultRouter()
v1_router.register('users', CustomUserViewSet, 'users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # получене confirmation code
    path('v1/auth/email/', views.obtain_conf_code),
    # получение токена
    path('v1/auth/token/', views.obtain_token),
    # обновление токена
    path('v1/token/refresh/', views.refresh_token, name='refresh_token'),
]
