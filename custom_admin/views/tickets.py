from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminUser
from tickets.models.ticket import Ticket
from tickets.serializers.tickets import TicketSerializer, TicketStatusSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    patch=extend_schema(
        summary="Назначение сотрудника на тикет",
    )
)
class TicketAssignView(UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['patch'] 

    def patch(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
    

@extend_schema_view(
    patch=extend_schema(
        summary="Обновление статуса тикета",
    )
)
class TicketUpdateStatusView(UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
    

class TicketListRetrieveView(RetrieveModelMixin, ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]