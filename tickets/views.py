from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from tickets.models.ticket import Ticket
from tickets.models.ticket_attachment import TicketAttachment
from tickets.models.ticket_comment import TicketComment
from tickets.serializers import TicketCommentSerializer, TicketListRetrieveSerializer, TicketSerializer, TicketStatusSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    get=extend_schema(
        summary="Список тикетов, созданных пользователем",
    ),
    post=extend_schema(
        summary="Создание нового тикета",
    )
)
class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        attachments = self.request.FILES.getlist('attachments')
        ticket = serializer.save()
        for file in attachments:
            TicketAttachment.objects.create(ticket=ticket, file=file)


@extend_schema_view(
    get=extend_schema(
        summary="Просмотр деталей тикета",
    )
)
class UserTicketsRetrieveView(generics.RetrieveAPIView):
    serializer_class = TicketListRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    

@extend_schema_view(
    patch=extend_schema(
        summary="Обновление статуса тикета",
    )
)
class TicketUpdateStatusView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
    

@extend_schema_view(
    post=extend_schema(
        summary="Создание комментария к тикету",
    ),
    get=extend_schema(
        summary="Список комментариев к тикету",
    ),
)
class TicketCommentView(generics.ListCreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TicketComment.objects.filter(ticket_id=self.kwargs['ticket_id'])

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            ticket_id=self.kwargs['ticket_id']
        )