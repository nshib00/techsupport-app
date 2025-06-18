from tickets.models.ticket_category import TicketCategory
from tickets.serializers.ticket_category import TicketCategorySerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from techsupport.exceptions import ConflictAPIException
from rest_framework import status
from users.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


@extend_schema_view(
    post=extend_schema(
        summary="Создание категории тикетов",
        responses={
            201: TicketCategorySerializer,
            400: OpenApiResponse(description="Некорректные данные для создания категории"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав для работы с категориями"),
            409: OpenApiResponse(description="Категория с заданным названием уже существует"),
        }
    ),
)
class TicketCategoryCreateView(CreateAPIView):
    serializer_class = TicketCategorySerializer
    queryset = TicketCategory.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        name = serializer.initial_data.get('name')
        category_with_name = TicketCategory.objects.filter(name__iexact=name)
        if category_with_name.exists():
            raise ConflictAPIException(
                {"name": "Категория с таким названием уже существует"},
            )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )