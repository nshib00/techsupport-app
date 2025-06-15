from rest_framework import serializers
from tickets.models.ticket import Ticket
from tickets.serializers.ticket_attachments import TicketAttachmentSerializer


class TicketSerializer(serializers.ModelSerializer):
    attachments = TicketAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'category', 'created_at', 'attachments']
        read_only_fields = ['attachments']


class TicketListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'status']