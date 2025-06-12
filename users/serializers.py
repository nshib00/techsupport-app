from rest_framework import serializers

from techsupport import settings


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}