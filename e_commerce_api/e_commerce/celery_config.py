from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_commerce.settings")
celery_app = Celery("e_commerce")

celery_app.conf.beat_schedule = {}
# Using a string here means the worker will not have to
# pickle the object when using Windows.
celery_app.config_from_object("django.conf:settings")
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
