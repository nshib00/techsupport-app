from rest_framework.generics import ListAPIView, UpdateAPIView
from users.models import User
from users.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer, UserRoleUpdateSerializer
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
            valid_roles = [choice[0] for choice in User.Role.choices]
            if role not in valid_roles:
                raise ValidationError({'role': f'Недопустимое значение. Возможные значения: {", ".join(valid_roles)}'})
            return User.objects.filter(role=role)
        return User.objects.all()
    

@extend_schema(
    summary="Изменение роли пользователя",
    description=(
        'Позволяет изменить роль пользователя с заданным ID, кроме себя.\n\n'
        'Доступные значения: user, support.\n\n'
        'Метод доступен **только для администраторов**.'
    ),
    responses={
        200: UserSerializer(many=True),
        400: OpenApiResponse(description='Некорректная роль пользователя'),
        401: OpenApiResponse(description="Пользователь не авторизован"),
        403: OpenApiResponse(description="Нет прав для изменения роли пользователя"),
        404: OpenApiResponse(description="Пользователь с указанным ID не найден"),
    }
)
class UserUpdateRoleView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRoleUpdateSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['patch']


