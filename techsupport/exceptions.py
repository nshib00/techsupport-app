from rest_framework.exceptions import APIException


class ConflictAPIException(APIException):
    status_code = 409
    default_detail = "Конфликт: ресурс уже существует"
    default_code = "conflict"