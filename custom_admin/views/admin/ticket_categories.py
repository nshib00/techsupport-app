from tickets.models.ticket_category import TicketCategory
from tickets.serializers.ticket_category import TicketCategorySerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


@extend_schema_view(
    post=extend_schema(
        summary="Создание категории тикетов",
        responses={
            201: TicketCategorySerializer,
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав для работы с категориями"),
        }
    ),
)
class TicketCategoryCreateView(CreateAPIView):
    serializer_class = TicketCategorySerializer
    queryset = TicketCategory.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]