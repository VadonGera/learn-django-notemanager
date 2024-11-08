from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
# from .apps import UsersConfig

# app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('api/', include(router.urls)),  # Добавляем маршруты для API
]