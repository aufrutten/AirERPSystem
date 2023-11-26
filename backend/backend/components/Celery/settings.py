from django.conf import settings


# Celery Configuration Options
REDIS_URL = "redis://redis-svc.developing:6379" if settings.DEBUG else "redis://redis-svc.production:6379"
CELERY_BROKER_URL = "redis://redis-svc.developing:6379" if settings.DEBUG else "redis://redis-svc.production:6379"
CELERY_RESULT_BACKEND = "redis://redis-svc.developing:6379" if settings.DEBUG else "redis://redis-svc.production:6379"
CELERY_TIMEZONE = settings.TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
