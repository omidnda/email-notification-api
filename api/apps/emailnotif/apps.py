from django.apps import AppConfig


class EmailnotifConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.emailnotif'
    
    def ready(self) -> None:
        from . import signals
        return super().ready()