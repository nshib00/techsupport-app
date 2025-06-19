from rest_framework import serializers
from notifications.models import Notification
from techsupport.common.serializers import BaseModelSerializer


class NotificationSerializer(BaseModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']