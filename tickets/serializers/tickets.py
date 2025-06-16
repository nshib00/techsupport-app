from rest_framework import serializers
from tickets.models.ticket import Ticket
from tickets.serializers.ticket_attachments import TicketAttachmentSerializer
from users.models import User


class TicketSerializer(serializers.ModelSerializer):
    attachments = TicketAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'category', 'assigned_to', 'created_at', 'attachments']
        read_only_fields = ['assigned_to', 'attachments']


class TicketListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'status']


class TicketAssignSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.SUPPORT),
        error_messages={
            'does_not_exist': 'Пользователь с таким ID не найден или не является сотрудником поддержки.',
            'invalid': 'Некорректный ID пользователя.'
        }
    )

    class Meta:
        model = Ticket
        fields = ['id', 'assigned_to']