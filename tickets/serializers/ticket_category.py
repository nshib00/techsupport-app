from rest_framework.serializers import ModelSerializer

from tickets.models.ticket_category import TicketCategory


class TicketCategorySerializer(ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'description']