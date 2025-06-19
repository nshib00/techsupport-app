from tickets.models import TicketHistory


class TicketHistoryMixin:
    """
    Добавляет историю изменений в модель Ticket.

    Использование:
    - Наследовать сериализатор от этого миксина.
    - В методе `update()` сериализатора до изменений в объекте instance 
      нужно вызвать `self.log_history(instance, validated_data)`.
    """
    def log_history(self, instance, validated_data):
        """
        Логирует изменения полей тикета.
        """
        self.context: dict # контекст - словарь с данными из сериализатора
        user = self.context['request'].user

        track_fields = ['subject', 'description', 'status', 'assigned_to', 'category']

        for field in track_fields:
            old_value = getattr(instance, field, None)
            new_value = validated_data.get(field, old_value)

            if field == 'assigned_to' and old_value and new_value:
                old_value_str = str(old_value.id) if old_value else ''
                new_value_str = str(new_value.id) if new_value else ''
            elif field == 'category' and old_value and new_value:
                old_value_str = getattr(old_value, 'name', str(old_value))
                new_value_str = getattr(new_value, 'name', str(new_value))
            else:
                old_value_str = str(old_value) if old_value is not None else ''
                new_value_str = str(new_value) if new_value is not None else ''

            if old_value != new_value:
                TicketHistory.objects.create(
                    ticket=instance,
                    changed_by=user,
                    field=field,
                    old_value=old_value_str,
                    new_value=new_value_str
                )
