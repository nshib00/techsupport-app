from rest_framework import serializers
from techsupport.common.serializers import BaseModelSerializer
from users.models import User


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
 

class UserCreateSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserShortSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']


class UserRoleUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role']
        read_only_fields = ['id']

    def validate_role(self, value):
        valid_roles = (User.Role.USER, User.Role.SUPPORT)
        if value not in valid_roles:
            raise serializers.ValidationError(
                {"role": f"Недопустимое значение роли. Допустимые значения: {', '.join(valid_roles)}."}
            )
        if self.instance and self.instance.role == User.Role.ADMIN:
            raise serializers.ValidationError(
                {"role": "Нельзя изменять роль администратора."}
            )
        return value

    def validate(self, data):
        request_user = self.context['request'].user
        if self.instance == request_user and data.get('role') != 'admin':
            raise serializers.ValidationError(
                {"role": "Вы не можете понизить свою собственную роль."}
            )
            
        return data

    