from rest_framework import serializers
from users.models import User
from techsupport import settings


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
 

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']