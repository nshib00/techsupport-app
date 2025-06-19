from techsupport.common.serializers import BaseModelSerializer
from tickets.models.ticket_attachment import TicketAttachment
from tickets.serializers.validators import validate_ticket_attachment



class TicketAttachmentSerializer(BaseModelSerializer):  
    class Meta:
        model = TicketAttachment
        fields = ['id', 'file', 'uploaded_at']

    def validate_file(self, value):
        validate_ticket_attachment(file=value)