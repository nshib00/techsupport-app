from rest_framework import serializers

from techsupport import settings


User = settings.AUTH_USER_MODEL


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
 

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}