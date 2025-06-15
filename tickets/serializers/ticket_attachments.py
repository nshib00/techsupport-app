from rest_framework.serializers import ModelSerializer
from tickets.models.ticket_attachment import TicketAttachment


class TicketAttachmentSerializer(ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = ['id', 'file', 'uploaded_at']