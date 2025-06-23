from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from tickets.models.ticket import Ticket
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from tickets.models.ticket_attachment import TicketAttachment
from tickets.serializers.ticket_attachments import TicketAttachmentSerializer
from tickets.serializers.consts import ALLOWED_EXTENSIONS
from tickets.serializers.tickets import TicketListRetrieveSerializer, TicketSerializer
from drf_spectacular.utils import (
    extend_schema_view, extend_schema, inline_serializer, OpenApiResponse, OpenApiParameter
)
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache


@extend_schema_view(
    get=extend_schema(
        summary="Список тикетов, созданных пользователем",
        description= "Возвращает список всех тикетов, созданных текущим пользователем.",
        parameters=[
            OpenApiParameter(
                name="status",
                description="Фильтр тикетов по статусу",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
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
            "Через поле `attachments` можно прикрепить один или несколько файлов как вложения.\n\n"
            f"Доступные форматы файлов: {', '.join(ALLOWED_EXTENSIONS)}. "
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
                        help_text="Файлы вложений (можно загрузить до 10)",
                        max_length=10
                    ),
                }
            )
        },
        responses={
            201: TicketSerializer,
            400: OpenApiResponse(description="Неверные данные или ошибка валидации"),
            401: OpenApiResponse(description="Пользователь не авторизован")
        }
    )
)
@method_decorator(
    cache_page(
        timeout=60 * 5,
        key_prefix='tickets_user_list'
    ), 
    name='get'
)
class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Ticket.objects.filter(user=self.request.user)
        status = self.request.GET.get('status')
        if status is not None:
            valid_status_names = [st[0] for st in Ticket.Status.choices]
            if status not in valid_status_names:
                raise ValidationError(
                    {'status': f'Недопустимое значение. Возможные значения: {", ".join(valid_status_names)}'}
                )
            return queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        attachments = self.request.FILES.getlist('attachments')
        if len(attachments) > 10:
            raise ValidationError(
                {'attachments': 'Нельзя загружать больше 10 вложений к обращению.'}
            )
        for file in attachments:
            attachment_serializer = TicketAttachmentSerializer(data={'file': file})
            attachment_serializer.is_valid(raise_exception=True)
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
    
    def retrieve(self, request, *args, **kwargs):
        ticket_id = kwargs.get("pk")
        cache_key = f"tickets_user_detail:{ticket_id}"

        data = cache.get(cache_key)
        if data:
            return Response(data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        cache.set(cache_key, serializer.data, timeout=60*15)
        return Response(serializer.data)



        