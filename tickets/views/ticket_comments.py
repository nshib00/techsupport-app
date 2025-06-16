from typing import cast
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from tickets.models.ticket_comment import TicketComment
from tickets.serializers.ticket_comments import TicketCommentSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiParameter
from users.models import User


@extend_schema_view(
    post=extend_schema(
        summary="Создание комментария к тикету",
        description=(
            "Создает новый комментарий к тикету с указанным ID. "
            "is_internal=True позволяет создать **внутренний** комментарий. "
            "Просматривать и создавать внутренние комментарии могут создавать только **администраторы** и **сотрудники поддержки**."
        ),
        responses={
            201: TicketCommentSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
            403: OpenApiResponse(description="Недостаточно прав доступа"),
        },
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID тикета, к которому нужно создать комментарий"
            ),
        ],
        request=TicketCommentSerializer
    ),
    get=extend_schema(
        summary="Список комментариев к тикету",
        description="Возвращает список комментариев, прикреплённых к тикету с указанным ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID тикета, для которого нужно получить комментарии"
            ),
        ],
        responses={
            200: TicketCommentSerializer(many=True),
            401: OpenApiResponse(description="Пользователь не авторизован"),
        }
    )
)
class TicketCommentView(generics.ListCreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TicketComment.objects.filter(ticket_id=self.kwargs['pk'], user=self.request.user)

    def perform_create(self, serializer):
        is_internal = serializer.validated_data.get('is_internal', False)

        # Приведение self.request.user к типу User. На исполнение кода не влияет, нужно для корректной подсветки и автодополнения в IDE
        user = cast(User, self.request.user)
         
        if is_internal:
            if user.role not in (User.Role.SUPPORT, User.Role.ADMIN):
                raise PermissionDenied("Недостаточно прав доступа.")
        serializer.save(
            user=self.request.user,
            ticket_id=self.kwargs['pk']
        )