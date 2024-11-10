import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Note
from .serializers import NoteSerializer


# Настраиваем логгер для приложения "notes"
logger = logging.getLogger("notes")


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Логируем запрос списка заметок
        logger.debug(
            "Пользователь с id %s запросил список своих заметок",
            self.request.user.id,
        )
        # Ограничиваем список заметок только для текущего пользователя
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Логируем создание новой заметки
        logger.info("Пользователь с id %s создает новую заметку", self.request.user.id)
        # Устанавливаем текущего пользователя как автора заметки
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # Логируем запрос на редактирование заметки
        note_id = kwargs.get("pk")
        logger.info(
            "Пользователь с id %s пытается обновить заметку с id %s",
            request.user.id,
            note_id,
        )

        try:
            response = super().update(request, *args, **kwargs)
            # Логируем успешное редактирование заметки
            logger.info(
                "Пользователь с id %s успешно обновил заметку с id %s",
                request.user.id,
                note_id,
            )
            return response
        except Exception as e:
            # Логируем ошибку при редактировании
            logger.error(
                "Ошибка при редактировании заметки с id %s пользователем с id %s: %s",
                note_id,
                request.user.id,
                str(e),
            )
            return Response(
                {"detail": "Ошибка при обновлении заметки."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        # Логируем запрос на удаление заметки
        note_id = kwargs.get("pk")
        logger.info(
            "Пользователь с id %s пытается удалить заметку с id %s",
            request.user.id,
            note_id,
        )

        try:
            response = super().destroy(request, *args, **kwargs)
            # Логируем успешное удаление заметки
            logger.info(
                "Пользователь с id %s успешно удалил заметку с id %s",
                request.user.id,
                note_id,
            )
            return response
        except Exception as e:
            # Логируем ошибку при удалении
            logger.error(
                "Ошибка при удалении заметки с id %s пользователем с id %s: %s",
                note_id,
                request.user.id,
                str(e),
            )
            return Response(
                {"detail": "Ошибка при удалении заметки."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
