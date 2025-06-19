from nh3 import clean as nh3_clean


class XSSProtectionMixin:
    ALLOWED_TAGS = {"b", "i", "u", "p", "br", "a"}  # разрешённые HTML-теги
    ALLOWED_ATTRIBUTES = {
        "a": {"href", "title", "target"},  # разрешённые атрибуты для тега <a>
    }

    def to_internal_value(self, data: dict):
        if hasattr(super(), 'to_internal_value'):
            validated_data: dict = super().to_internal_value(data) # стандартная валидация DRF # type: ignore
        else:
            validated_data = data
        for field_name, field_value in validated_data.items():
            if isinstance(field_value, str): # очищаются все строковые поля
                validated_data[field_name] = nh3_clean(field_value)
        return validated_data