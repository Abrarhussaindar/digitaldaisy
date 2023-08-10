# settings.py

CELERY_BROKER_URL = 'redis://your-redis-host:your-redis-port/0'
CELERY_RESULT_BACKEND = 'redis://your-redis-host:your-redis-port/0'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
