from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    is_completed = serializers.BooleanField(default=False)
    priority = serializers.IntegerField(default=0)

    def create(self, data):
        return Task(**data)
