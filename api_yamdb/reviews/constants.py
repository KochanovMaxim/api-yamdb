# reviews/constants.py - добавляем константы для пользователей

# Для названий
CHARFIELD_NAME_MAX_LENGTH = 256
CHARFIELD_SLUG_MAX_LENGTH = 50

# Для оценок
SCORE_MIN_VALUE = 1
SCORE_MAX_VALUE = 10

# Для обрезки текста
STR_TEXT_TRUNCATE_CHARS = 50

# Для валидации годов
FIRST_FILM = 1888  # год первого фильма

# Для пользователей (добавляем)
USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254
ROLE_MAX_LENGTH = 20
BIO_MAX_LENGTH = 500

# Регулярные выражения
USERNAME_REGEX = r'^[\w.@+-]+\Z'

# Запрещенное имя пользователя
FORBIDDEN_USERNAME = 'me'

# Роли пользователей
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = [
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
]
