from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminUser
from tickets.models.ticket import Ticket
from tickets.serializers import TicketSerializer
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