from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from . import scheduler
        from django.db.utils import OperationalError, ProgrammingError

        try:
            scheduler.setup_periodic_tasks()
        except (OperationalError, ProgrammingError):
            pass
