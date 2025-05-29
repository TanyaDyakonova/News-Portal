from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

class Command(BaseCommand):
    help = 'Создаёт задачу еженедельной рассылки по категориям'

    def handle(self, *args, **kwargs):
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='8',
            day_of_week='1',
            timezone='UTC',
        )

        task, created = PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name='weekly_category_digest',
            task='news.tasks.send_weekly_subscriber_news',
            defaults={
                'args': json.dumps([]),
                'enabled': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Задача создана'))
        else:
            self.stdout.write(self.style.WARNING('Задача уже существует'))
