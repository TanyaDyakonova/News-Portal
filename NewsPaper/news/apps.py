from django.apps import AppConfig

class NewsConfig(AppConfig):
    name = 'news'

    def ready(self):
        from .tasks import start_scheduler
        start_scheduler()