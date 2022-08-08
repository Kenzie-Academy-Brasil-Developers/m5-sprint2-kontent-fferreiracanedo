from rest_framework import serializers

from content.models import Content


class ContentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    module = serializers.CharField(max_length=100)
    students = serializers.IntegerField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()

    def create(self, validated_data: dict):
        return Content.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
