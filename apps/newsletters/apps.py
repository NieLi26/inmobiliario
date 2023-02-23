from django.apps import AppConfig


class NewslettersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.newsletters"

    def ready(self):
        from . import signals
