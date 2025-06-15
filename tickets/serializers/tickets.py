from rest_framework import serializers
from tickets.models.ticket import Ticket


class TicketSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'category', 'created_at', 'attachments']


class TicketListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'status']