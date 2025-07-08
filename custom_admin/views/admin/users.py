from rest_framework.generics import ListAPIView, UpdateAPIView
from users.models import User
from users.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer, UserRoleUpdateSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.exceptions import ValidationError
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend


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
@method_decorator(
    cache_page(
        timeout=60 * 5,
        key_prefix='users_list'
    ),
    name='get'
)
class UserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']
    queryset = User.objects.all()


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


