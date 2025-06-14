from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from users.permissions import IsAdminUser
from tickets.models.ticket import Ticket
from tickets.serializers.tickets import TicketSerializer, TicketStatusSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

@extend_schema_view(
    patch=extend_schema(
        summary="Назначение сотрудника на тикет",
        responses={
            200: TicketSerializer,
            400: OpenApiResponse(description="Неверные данные"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав для изменения тикета"),
            404: OpenApiResponse(description="Тикет не найден"),
        }
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
        responses={
            200: TicketSerializer,
            400: OpenApiResponse(description="Неверные данные"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Нет прав для изменения тикета"),
            404: OpenApiResponse(description="Тикет не найден"),
        }
    )
)
class TicketUpdateStatusView(UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
    

@extend_schema_view(
    list=extend_schema(
        summary="Получение списка тикетов",
        parameters=[
            OpenApiParameter(
                name='status',
                description='Фильтрация по статусу тикета (например: open, closed)',
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
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

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
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            raise NotFound(detail="Ticket not found.")

        serializer = self.get_serializer(instance)
        return Response(serializer.data)