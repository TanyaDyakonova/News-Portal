from django.db.models.signals import post_migrate
from django.dispatch import receiver
from . import scheduler

@receiver(post_migrate)
def setup_periodic_tasks(sender, **kwargs):
    scheduler.setup_periodic_tasks()
