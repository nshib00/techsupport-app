ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.txt', '.log', '.docx', '.xlsx', '.csv', '.pdf']

ALLOWED_MIME_TYPES = [
    'image/jpeg', 'image/png', 'image/webp',
    'text/plain',
    'text/csv',
    'application/pdf',
    'application/zip', # для распознавания .xlsx и .csv файлов
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document' # для .docx-файла
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' # для .xlsx-файла
]
