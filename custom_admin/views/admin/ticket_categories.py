from tickets.models.ticket_category import TicketCategory
from tickets.serializers.ticket_category import TicketCategorySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from techsupport.exceptions import ConflictAPIException
from users.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


from drf_spectacular.utils import OpenApiParameter

@extend_schema_view(
    create=extend_schema(
        summary="Создание категории тикетов",
        request=TicketCategorySerializer,
        responses={
            201: TicketCategorySerializer,
            400: OpenApiResponse(description="Некорректные данные для создания категории"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав для работы с категориями"),
            409: OpenApiResponse(description="Категория с заданным названием уже существует"),
        }
    ),
    partial_update=extend_schema(
        summary="Обновление категории тикетов",
        request=TicketCategorySerializer,
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID категории, которую необходимо обновить'
            )
        ],
        responses={
            200: TicketCategorySerializer,
            400: OpenApiResponse(description="Некорректные данные"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав для обновления категорий"),
            404: OpenApiResponse(description="Категория не найдена"),
            409: OpenApiResponse(description="Категория с таким названием уже существует"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление категории тикетов",
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='ID категории, которую необходимо удалить'
            )
        ],
        responses={
            204: OpenApiResponse(description="Категория удалена"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав на удаление категории"),
            404: OpenApiResponse(description="Категория не найдена"),
        },
    ),
)
class TicketCategoryViewSet(ModelViewSet):
    serializer_class = TicketCategorySerializer
    queryset = TicketCategory.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['post', 'patch', 'delete']

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        category_with_name = TicketCategory.objects.filter(name__iexact=name)
        if category_with_name.exists():
            raise ConflictAPIException(
                {"name": "Категория с таким названием уже существует"},
            )
        return super().create(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        category = self.get_object()
        new_name = request.data.get('name')
        category_with_new_name_exists: bool = TicketCategory.objects.exclude(
            pk=category.pk
        ).filter(name__iexact=new_name).exists()
        if new_name and category_with_new_name_exists:
            raise ConflictAPIException({"name": "Категория с таким названием уже существует"})
        return super().partial_update(request, *args, **kwargs)