from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from django_filters import rest_framework as filters


@extend_schema_view(
    get=extend_schema(
        summary="Cписок уведомлений пользователя",
        description="Возвращает список уведомлений, отсортированных по дате создания (по убыванию).",
        responses=NotificationSerializer(many=True),
        parameters=[
        OpenApiParameter(
            name='is_read',
            description='Прочитано/не прочитано',
            required=False,
            type=bool
        )
    ],
    )
)
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['is_read']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    

@extend_schema_view(
    patch=extend_schema(
        summary="Пометить уведомление как прочитанное",
        description="Ставит флаг is_read уведомления в значение True.",
        responses=NotificationSerializer(many=True),
    )
)
class NotificationUpdateView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    http_method_names = ['patch']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)