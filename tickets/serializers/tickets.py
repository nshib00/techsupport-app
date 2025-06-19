from rest_framework import serializers
from tickets.models.ticket import Ticket
from tickets.serializers.ticket_attachments import TicketAttachmentSerializer
from users.models import User
from datetime import datetime


class TicketSerializer(serializers.ModelSerializer):
    attachments = TicketAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'category', 'status', 'attachments']
        read_only_fields = ['assigned_to', 'status', 'attachments']


class TicketListAdminSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = [
            'assigned_to', 'status', 'attachments', 'created_at', 'updated_at', 'closed_at', 'closed_by'
        ]


class TicketListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'status', 'updated_at', 'closed_at', 'closed_by']
        read_only_fields = ['updated_at', 'closed_at', 'closed_by']

    def update(self, instance, validated_data):
        new_status = validated_data.get('status')
        old_status = instance.status

        instance.status = new_status

        if new_status == Ticket.Status.CLOSED and old_status != Ticket.Status.CLOSED:
            instance.closed_at = datetime.now()
            instance.closed_by = self.context['request'].user
        else:
            instance.closed_at = None
            instance.closed_by = None

        instance.save()
        return instance


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