from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from tickets.models.ticket import Ticket
from rest_framework.exceptions import NotFound
from tickets.models.ticket_attachment import TicketAttachment
from tickets.serializers.tickets import TicketListRetrieveSerializer, TicketSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer, OpenApiResponse, OpenApiParameter


@extend_schema_view(
    get=extend_schema(
        summary="Список тикетов, созданных пользователем",
        description= "Возвращает список всех тикетов, созданных текущим пользователем.",
        responses={
            200: TicketSerializer(many=True),
            401: OpenApiResponse(description="Пользователь не авторизован")
        }
    ),
    post=extend_schema(
        summary="Создание нового тикета",
        description=(
            "Позволяет создать новый тикет в службу технической поддержки. "
            "Поля `subject`, `category` и `description` обязательны.\n\n"
            "Можно прикрепить один или несколько файлов как вложения. "
            "Файлы отправляются в формате multipart/form-data."
        ),
        request={
            'multipart/form-data': inline_serializer(
                name='TicketCreateRequest',
                fields={
                    'subject': serializers.CharField(),
                    'category': serializers.IntegerField(),
                    'description': serializers.CharField(),
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
        description=(
            "Возвращает подробную информацию о тикете пользователя по его ID.\n\n"
            "Доступ разрешён только владельцу тикета. Если тикет не найден "
            "или принадлежит другому пользователю, будет возвращён ответ 404."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="ID тикета",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            200: TicketListRetrieveSerializer,
            401: OpenApiResponse(description="Пользователь не аутентифицирован."),
            404: OpenApiResponse(description="Тикет не найден."),
        }
    )
)
class UserTicketsRetrieveView(generics.RetrieveAPIView):
    serializer_class = TicketListRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
    
    def get_object(self):
        ticket_id = self.kwargs.get("pk")
        try:
            ticket = Ticket.objects.get(pk=ticket_id, user=self.request.user)
        except Ticket.DoesNotExist:
            raise NotFound("Тикет не найден.")
        return ticket



        