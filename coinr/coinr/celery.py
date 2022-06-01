from __future__ import absolute_import

import os
import ssl

from celery import Celery
from django.conf import settings
import environ

# set and read the .env file for environment variables
env = environ.Env()
environ.Env.read_env()

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coinr.settings')

app = Celery('coinr')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    BROKER_URL=env.str('REDIS_TLS_URL', 'rediss://redis:6379/0'),
    CELERY_RESULT_BACKEND=env.str('REDIS_TLS_URL', 'rediss://redis:6379/0'),
    task_routes={
        'coinr.service.handle_csv': {'queue': 'coin-tasks'},
        'coinr.service.handle_json': {'queue': 'coin-tasks'},
    },
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    }
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
