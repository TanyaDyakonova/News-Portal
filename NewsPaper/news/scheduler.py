from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

def setup_periodic_tasks():
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='8',
        day_of_week='1',
        day_of_month='*',
        month_of_year='*',
    )

    if not PeriodicTask.objects.filter(name='Weekly News Digest').exists():
        PeriodicTask.objects.create(
            crontab=schedule,
            name='Weekly News Digest',
            task='news.tasks.weekly_newsletter',
            args=json.dumps([]),
        )
