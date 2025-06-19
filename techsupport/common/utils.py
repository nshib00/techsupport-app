from nh3 import clean as nh3_clean



def sanitize_html(value: str) -> str:
    ALLOWED_TAGS = {"b", "i", "u", "p", "br", "a"}  # разрешённые HTML-теги
    ALLOWED_ATTRIBUTES = {
        "a": {"href", "title", "target"},  # разрешённые атрибуты для тега <a>
    }
    return nh3_clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES
    )
