from os import environ


# EMAIL SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = environ.get('EMAIL_ADDRESS')
DEFAULT_FROM_EMAIL = environ.get('EMAIL_ADDRESS')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_PASSWORD')
