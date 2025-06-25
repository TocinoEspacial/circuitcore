from django.apps import AppConfig


class YgvConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ygv'

def ready(self):
    import ygv.signals