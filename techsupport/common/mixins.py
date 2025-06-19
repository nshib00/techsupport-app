from techsupport.common.utils import sanitize_html


class XSSProtectionMixin:
    def to_internal_value(self, data: dict):
        if hasattr(super(), 'to_internal_value'):
            validated_data: dict = super().to_internal_value(data) # стандартная валидация DRF # type: ignore
        else:
            validated_data = data
        for field_name, field_value in validated_data.items():
            if isinstance(field_value, str): # очищаются все строковые поля
                validated_data[field_name] = sanitize_html(field_value)
        return validated_data