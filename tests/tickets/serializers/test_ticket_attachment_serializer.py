import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from tickets.serializers.ticket_attachments import TicketAttachmentSerializer
from rest_framework.exceptions import ValidationError
from tickets.serializers.validators import validate_ticket_attachment


# допустимое расширение и MIME
VALID_FILE_CONTENT = b"Binary data for test"
VALID_FILE = SimpleUploadedFile("test.txt", VALID_FILE_CONTENT, content_type="text/plain")

# слишком большой файл
TOO_BIG_FILE = SimpleUploadedFile(
    "big.txt",
    b"x" * 6 * 1024 * 1024,  # 6MB
    content_type="text/plain"
)

# недопустимое расширение
INVALID_EXT_FILE = SimpleUploadedFile("test.hgfhg", VALID_FILE_CONTENT, content_type="application/octet-stream")

# недопустимый mime (тип файла будет определён как None)
INVALID_MIME_FILE = SimpleUploadedFile("test.txt", b"", content_type="application/octet-stream")


@pytest.mark.django_db
def test_valid_attachment():
    validated_file = validate_ticket_attachment(VALID_FILE)
    assert validated_file is VALID_FILE


def test_file_too_large_error():
    with pytest.raises(ValidationError, match="объем не более 5 Мб"):
        validate_ticket_attachment(TOO_BIG_FILE)


def test_invalid_extension_error():
    with pytest.raises(ValidationError, match="Недопустимый тип файла"):
        validate_ticket_attachment(INVALID_EXT_FILE)


def test_invalid_mime_type_error():
    with pytest.raises(ValidationError, match="Недопустимый MIME-тип файла"):
        validate_ticket_attachment(INVALID_MIME_FILE)


@pytest.mark.django_db
def test_ticket_attachment_serializer_valid():
    serializer = TicketAttachmentSerializer(data={"file": VALID_FILE})
    assert serializer.is_valid(), serializer.errors
