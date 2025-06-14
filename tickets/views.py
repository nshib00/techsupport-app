from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from tickets.models.ticket import Ticket
from tickets.models.ticket_attachment import TicketAttachment
from tickets.models.ticket_comment import TicketComment
from tickets.serializers.tickets import TicketListRetrieveSerializer, TicketSerializer
from tickets.serializers.ticket_comments import TicketCommentSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer, OpenApiResponse


@extend_schema_view(
    get=extend_schema(
        summary="Список тикетов, созданных пользователем",
        responses={
            200: TicketSerializer(many=True),
            401: OpenApiResponse(description="Пользователь не авторизован")
        }
    ),
    post=extend_schema(
        summary="Создание нового тикета",
        request={
            'multipart/form-data': inline_serializer(
                name='TicketCreateRequest',
                fields={
                    'subject': serializers.CharField(),
                    'description': serializers.CharField(),
                    'category': serializers.IntegerField(),
                    'attachments': serializers.ListField(
                        child=serializers.FileField(),
                        required=False,
                        help_text="Файлы вложений (можно загрузить несколько)"
                    ),
                }
            )
        },
        responses={
            201: TicketSerializer,
            400: OpenApiResponse(description="Неверные данные"),
            401: OpenApiResponse(description="Пользователь не авторизован")
        }
    )
)
class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        attachments = self.request.FILES.getlist('attachments')
        ticket = serializer.save(user=self.request.user)
        for file in attachments:
            TicketAttachment.objects.create(ticket=ticket, user=self.request.user, file=file)


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


# class Ticket