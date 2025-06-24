from rest_framework import serializers
from tickets.serializers.consts import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES
import filetype


def validate_ticket_attachment(file):
    # проверка размера файла
    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise serializers.ValidationError(f"Загружаемый файл должен иметь объем не более {max_size_mb} Мб.")
        
    # проверка расширения файла
    import os
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise serializers.ValidationError(f"Недопустимый тип файла: {file_extension}")

    # проверка mime-типа файла
    header = file.read(261) # библиотека filetype использует до 261 начальных байт файла для определения его MIME-типа 
    kind = filetype.guess(header) 
    file.seek(0) # возврат указателя файла в начало

    if kind:
        mime_type = kind.mime 
    elif file_extension in ['.txt', '.log'] and header.strip(): # допускаем text/plain только если файл не пуст
        mime_type = 'text/plain'
    else:
        mime_type = None

    if mime_type not in ALLOWED_MIME_TYPES:
        raise serializers.ValidationError(f"Недопустимый MIME-тип файла: {mime_type or '(не определён)'}")

    return file