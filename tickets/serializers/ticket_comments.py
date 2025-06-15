from rest_framework.serializers import ModelSerializer
from tickets.models.ticket_comment import TicketComment


class TicketCommentSerializer(ModelSerializer):
    class Meta:
        model = TicketComment
        fields = ['id', 'message', 'is_internal', 'created_at']