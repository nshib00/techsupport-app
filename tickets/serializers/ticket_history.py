from techsupport.common.serializers import BaseModelSerializer
from tickets.models.ticket_history import TicketHistory


class TicketHistorySerializer(BaseModelSerializer):
    class Meta:
        model = TicketHistory
        fields = '__all__'