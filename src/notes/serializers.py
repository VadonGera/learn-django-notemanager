from rest_framework import serializers
from .models import Note
from users.serializers import UserSerializer


class NoteSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    author = serializers.CharField(source='user.__str__', read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'author']
