from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from tickets.models.ticket_category import TicketCategory
from tickets.serializers.ticket_category import TicketCategorySerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


@extend_schema_view(
    get=extend_schema(
        summary="Список всех категорий тикетов",
        responses={
            200: TicketCategorySerializer,
            401: OpenApiResponse(description="Пользователь не авторизован"),
        }
    ),
)
@method_decorator(
    cache_page(
        timeout=60 * 60 * 24,
        key_prefix='ticket_categories'
    ),
    name='get'
)
class TicketCategoryListView(ListAPIView):
    serializer_class = TicketCategorySerializer
    queryset = TicketCategory.objects.all()
    permission_classes = [IsAuthenticated]