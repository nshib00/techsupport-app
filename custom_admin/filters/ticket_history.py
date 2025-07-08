from django_filters.rest_framework import FilterSet, DateTimeFilter, NumberFilter, CharFilter
from tickets.models import TicketHistory


class TicketHistoryFilter(FilterSet):
    ticket = NumberFilter(
        field_name="ticket", lookup_expr="exact", label="ID тикета"
    )
    changed_by = NumberFilter(
        field_name="changed_by", lookup_expr="exact", label="Изменено пользователем (ID)"
    )
    field = CharFilter(
        field_name="field",
        lookup_expr="exact",
        label=(
            "Измененное поле (возможные варианты: " 
            "assigned_to, status, subject, description)"
        )
    )
    changed_at__gte = DateTimeFilter(field_name="changed_at", lookup_expr="gte", label="Дата изменения с")
    changed_at__lte = DateTimeFilter(field_name="changed_at", lookup_expr="lte", label="Дата изменения по")

    class Meta:
        model = TicketHistory
        fields = {
            'ticket': ['exact'],
            'changed_by': ['exact'],
            'field': ['exact'],
            'changed_at': ['gte', 'lte'],
        }