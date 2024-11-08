from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
