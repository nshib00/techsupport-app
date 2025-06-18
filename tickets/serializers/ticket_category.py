from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from tickets.models.ticket_category import TicketCategory


class TicketCategorySerializer(ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'description']  

    def validate_name(self, value):
        if TicketCategory.objects.filter(name__iexact=value).exists():
            raise ValidationError(
                "Категория с таким названием уже существует",
                code='unique'
            )
        return value