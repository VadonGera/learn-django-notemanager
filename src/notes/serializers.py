from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="user.__str__", read_only=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "user",
            "author",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user", "author"]
