from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from datetime import datetime
from users.permissions import IsSupportUser
from tickets.models.ticket import Ticket
from tickets.serializers.tickets import (
    TicketAssignSerializer, TicketListAdminSerializer, TicketSerializer, TicketStatusSerializer
)
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from notifications.tasks import send_status_change_notification_email
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache


@extend_schema_view(
    patch=extend_schema(
        summary="Назначение сотрудника на тикет",
        description="Позволяет назначить сотрудника поддержки на тикет по его ID.",
        request=TicketAssignSerializer,
        responses={
            200: OpenApiResponse(response=TicketAssignSerializer, description="Сотрудник успешно назначен"),
            400: OpenApiResponse(description="Ошибка валидации"),
            401: OpenApiResponse(description="Неавторизованный пользователь"),
            403: OpenApiResponse(description="Доступ запрещён"),
            404: OpenApiResponse(description="Тикет или пользователь не найден"),
        }
    )
)
class TicketAssignView(UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketAssignSerializer
    permission_classes = [IsSupportUser, IsAuthenticated]
    http_method_names = ['patch']
    

@extend_schema_view(
    patch=extend_schema(
        summary="Обновление статуса тикета",
        responses={
            200: TicketSerializer,
            400: OpenApiResponse(description="Неверные данные"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав для изменения тикета"),
            404: OpenApiResponse(description="Тикет не найден или передан несуществующий статус"),
        }
    )
)
class TicketUpdateStatusView(UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketStatusSerializer
    permission_classes = [IsSupportUser, IsAuthenticated]
    http_method_names = ['patch']

    def perform_update(self, serializer):
        ticket = self.get_object()
        old_status = ticket.status

        if ticket.assigned_to is None:
            raise ValidationError(
                {'assigned_to': 'Нельзя изменить статус, пока не назначен ответственный сотрудник.'}
            )

        instance = serializer.save()

        if instance.status == Ticket.Status.CLOSED:
            instance.closed_at = datetime.now()
            instance.closed_by = self.request.user
            instance.save(update_fields=['closed_at', 'closed_by'])
        
        send_status_change_notification_email.delay( # вызываем асинхронную задачу Celery для отправки уведомления
            ticket_id=instance.id,
            old_status=old_status,
            new_status=instance.status
        )
    

@extend_schema_view(
    list=extend_schema(
        summary="Получение списка тикетов",
        parameters=[
            OpenApiParameter(
                name='status',
                description='Фильтрация по статусу тикета (open, in_progress, resolved, closed)',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='assigned_to',
                description='ID пользователя, которому назначен тикет',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='category',
                description='ID категории тикета',
                required=False,
                type=int
            ),
        ],
        responses={
            200: TicketSerializer(many=True),
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав для просмотра тикетов"),
        }
    ),
    retrieve=extend_schema(
        summary="Получение одного тикета по ID",
        responses={
            200: TicketSerializer,
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав для просмотра тикета"),
            404: OpenApiResponse(description="Тикет не найден"),
        }
    )
)
class TicketListRetrieveView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = TicketListAdminSerializer
    permission_classes = [IsSupportUser, IsAuthenticated]

    def get_queryset(self):
        filters = {
            'status': self.request.GET.get('status'),
            'assigned_to': self.request.GET.get('assigned_to'),
            'category': self.request.GET.get('category'),
        }

        filters = {
            key: value for key, value in filters.items() if value is not None
        } # удаление пар со значением None

        return Ticket.objects.filter(**filters)
    
    @method_decorator(
        cache_page(
            timeout=60 * 5,
            key_prefix='tickets_support_list'
        ),
        name='get'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        # используется ручное кэширование для назначения читаемых префиксов (id тикета),
        # чтобы можно было при изменении конкретного тикета удалять очищать отдельно его кэш по префиксу
        cache_key = f"tickets_support_detail:{pk}"
        data = cache.get(cache_key)
        if data:
            return Response(data)

        try:
            instance = self.get_object()
        except Http404:
            raise NotFound("Ticket not found.")

        serializer = self.get_serializer(instance)
        cache.set(cache_key, serializer.data, timeout=60*15)
        return Response(serializer.data)