import logging
from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import (
    UserRegistrationSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)


User = get_user_model()

# Настраиваем логгер для приложения "users"
logger = logging.getLogger("users")


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Создаем копию данных для логирования
        log_data = request.data.copy()
        # Заменяем значение поля 'password' на 'secret_information'
        if "password" in log_data:
            log_data["password"] = "secret_information"

        # Логируем запрос на регистрацию
        logger.info(
            "Получен запрос на регистрацию пользователя с данными: %s", log_data
        )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Если данные валидны, сохраняем пользователя
            user = serializer.save()
            # Логируем успешную регистрацию
            logger.info("Пользователь успешно зарегистрирован с id: %s", user.id)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            # Логируем ошибки валидации при неудачной регистрации
            logger.warning(
                "Ошибка регистрации пользователя. Ошибки валидации: %s",
                serializer.errors,
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        # Логируем запрос на получение списка пользователей
        logger.info(
            "Получен запрос на список пользователей от пользователя: %s", request.user
        )

        try:
            # Получаем список пользователей и сериализуем
            response = super().list(request, *args, **kwargs)
            # Логируем успешный результат
            logger.info(
                "Список пользователей успешно отправлен. Количество пользователей: %d",
                len(response.data),
            )
            return response
        except Exception as e:
            # Логируем возможные ошибки при выполнении запроса
            logger.error("Ошибка при получении списка пользователей: %s", str(e))
            return Response(
                {"detail": "Ошибка при получении списка пользователей."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def update(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        current_user = request.user

        # Логируем попытку редактирования
        logger.info(
            "Пользователь с id %s запросил редактирование пользователя с id %s",
            current_user.id,
            user_id,
        )

        # Проверяем, есть ли у пользователя права на редактирование указанного пользователя
        if not current_user.is_superuser and current_user.id != user_id:
            # Логируем попытку несанкционированного доступа
            logger.warning(
                "Пользователь с id %s попытался изменить данные другого пользователя с id %s",
                current_user.id,
                user_id,
            )
            raise PermissionDenied("Редактирование чужого профиля запрещено")

        try:
            # Пытаемся обновить данные пользователя
            response = super().update(request, *args, **kwargs)
            # Логируем успешное редактирование
            logger.info(
                "Пользователь с id %s успешно изменил данные пользователя с id %s",
                current_user.id,
                user_id,
            )
            return response

        except Exception as e:
            # Логируем ошибку при редактировании
            logger.error(
                "Ошибка при редактировании пользователя с id %s пользователем с id %s: %s",
                user_id,
                current_user.id,
                str(e),
            )
            return Response(
                {"detail": "Ошибка при редактировании пользователя."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
