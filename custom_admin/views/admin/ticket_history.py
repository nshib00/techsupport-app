from custom_admin.filters.ticket_history import TicketHistoryFilter
from tickets.models.ticket_history import TicketHistory
from tickets.serializers.ticket_history import TicketHistorySerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


@extend_schema_view(
    get=extend_schema(
        summary="Просмотр истории изменения тикетов",
        description=(
            "Позволяет получить список изменений, связанных с тикетами.\n\n"
            "Доступна фильтрация по следующим параметрам:\n"
            "- **ticket** — ID тикета;\n"
            "- **changed_by** — ID пользователя, который внёс изменения;\n"
            "- **field** — название изменённого поля;\n"
            "- **changed_at__gte** — дата и время начала интервала изменений;\n"
            "- **changed_at__lte** — дата и время конца интервала изменений."
        ),
        request=TicketHistorySerializer(many=True),
        responses={
            200: TicketHistorySerializer,
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав для просмотра истории изменений тикетов"),
        }
    )
)
class TicketHistoryView(ListAPIView):
    queryset = TicketHistory.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = TicketHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketHistoryFilter