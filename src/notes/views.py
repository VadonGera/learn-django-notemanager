from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как автора заметки
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Ограничиваем список заметок только для текущего пользователя
        return Note.objects.filter(user=self.request.user)
