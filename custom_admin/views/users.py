from rest_framework.generics import ListAPIView
from users.models import User
from users.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.exceptions import ValidationError


@extend_schema(
    summary="Список всех пользователей с фильтрацией по роли",
    parameters=[
        OpenApiParameter(
            name='role',
            description='Фильтрация пользователей по роли (список ролей: admin, user, support)',
            required=False,
            type=str
        )
    ],
    responses={
        200: UserSerializer(many=True),
        400: OpenApiResponse(description='Некорректный параметр запроса'),
        401: OpenApiResponse(description="Пользователь не авторизован"),
        403: OpenApiResponse(description="Нет прав для просмотра списка пользователей"),
        500: OpenApiResponse(description='Внутренняя ошибка сервера'),
    }
)
class UserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_queryset(self):
        role = self.request.GET.get('role')
        if role is not None:
            valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
            if role not in valid_roles:
                raise ValidationError({'role': f'Недопустимое значение. Возможные значения: {", ".join(valid_roles)}'})
            return User.objects.filter(role=role)
        return User.objects.all()