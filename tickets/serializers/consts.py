ALLOWED_EXTENSIONS = [
    '.jpg', '.jpeg', '.png', '.webp', '.txt', '.log', '.docx', '.pdf', '.xlsx'
]

ALLOWED_MIME_TYPES = [
    'image/jpeg', 'image/png', 'image/webp',
    'text/plain',
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document', # для .docx-файла
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', # для .xlsx-файла
    'application/zip', # иногда .docx и .xlsx файлы распознаются как application/zip
]
