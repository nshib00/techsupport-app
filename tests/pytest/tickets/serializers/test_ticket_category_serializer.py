import pytest
from tickets.models.ticket_category import TicketCategory
from tickets.serializers.ticket_category import TicketCategorySerializer


@pytest.mark.django_db
def test_ticket_category_serializer_valid():
    serializer = TicketCategorySerializer(data={'name': 'Категория', 'description': 'Обращения'})
    assert serializer.is_valid(), serializer.errors
    validated_data: dict = serializer.validated_data # type: ignore
    assert validated_data['name'] == 'Категория'


@pytest.mark.django_db
def test_ticket_category_duplicate_error():
    TicketCategory.objects.create(name='Ошибки', description='Системные сбои')

    serializer = TicketCategorySerializer(data={'name': 'Ошибки', 'description': 'Дублирование'})
    assert not serializer.is_valid()
    assert 'name' in serializer.errors
    assert serializer.errors['name'][0].code == 'unique'