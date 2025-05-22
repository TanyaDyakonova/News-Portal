from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Category, Post

def send_weekly_updates():
    now = timezone.now()
    last_week = now - timezone.timedelta(days=7)
    for category in Category.objects.all():
        posts = Post.objects.filter(categories=category, created_at__gte=last_week)
        if posts.exists():
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                subject = f"Еженедельные новости категории «{category.name}»"
                html_content = render_to_string('weekly_update.html', {'posts': posts, 'subscriber': subscriber})
                send_mail(subject, '', 'tanyamars16@yandex.ru', [subscriber.email], html_message=html_content)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_weekly_updates, 'cron', day_of_week='mon', hour=8, minute=0)
    scheduler.start()