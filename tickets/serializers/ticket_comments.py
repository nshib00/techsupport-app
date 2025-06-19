from techsupport.common.serializers import BaseModelSerializer
from tickets.models.ticket_comment import TicketComment


class TicketCommentSerializer(BaseModelSerializer):
    class Meta:
        model = TicketComment
        fields = ['id', 'message', 'is_internal', 'created_at']
        read_only_fields = ['created_at']