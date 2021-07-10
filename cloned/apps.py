from django.apps import AppConfig


class ClonedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cloned'
