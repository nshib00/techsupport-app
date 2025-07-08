from django_filters. rest_framework import FilterSet, CharFilter
from .models import TicketCategory

class TicketCategoryFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = TicketCategory
        fields = ['name']
