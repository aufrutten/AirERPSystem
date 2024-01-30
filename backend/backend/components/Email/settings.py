from decouple import config

# EMAIL SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_ADDRESS", default="", cast=str)
DEFAULT_FROM_EMAIL = config("EMAIL_ADDRESS", default="", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD", default="", cast=str)
