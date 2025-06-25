from rest_framework.views import exception_handler as drf_default
from rest_framework.exceptions import ValidationError
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def drf_exception_handler(exc, context):
    response = drf_default(exc, context)
    view = context.get('view')

    if isinstance(exc, ValidationError) and response is not None:
        if _has_unique_error(exc.detail):
            response.status_code = status.HTTP_409_CONFLICT

    logger.warning(
        f"Exception in view: {view.__class__.__name__ if view else 'unknown'}: {exc}"
    )

    return response


def _has_unique_error(detail):
    # рекурсивный поиск ошибки с кодом 'unique' в словаре/списке ошибок

    if isinstance(detail, list):
        return any(_has_unique_error(item) for item in detail)
    if isinstance(detail, dict):
        return any(_has_unique_error(item) for item in detail.values())
    return getattr(detail, 'code', None) == 'unique'
