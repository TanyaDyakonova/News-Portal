from celery import shared_task
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post, Category

@shared_task
def weekly_newsletter():
    today = now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)

    if not posts.exists():
        return

    subject = 'Weekly News Digest'
    message = '\n\n'.join([f'{p.title}\nhttp://127.0.0.1:8000/news/{p.pk}/' for p in posts])

    for user in User.objects.all():
        send_mail(
            subject,
            message,
            from_email='tanyamars16@yandex.ru',
            recipient_list=[user.email],
            fail_silently=False,
        )


@shared_task
def send_weekly_subscriber_news():
    today = timezone.now()
    last_week = today - timedelta(days=7)

    categories = Category.objects.all()

    for category in categories:
        posts = Post.objects.filter(
            categories=category,
            created_at__gte=last_week,
            created_at__lte=today
        )

        if not posts.exists():
            continue

        subscribers = category.subscribers.all()

        for user in subscribers:
            html_content = render_to_string(
                'weekly_update.html',
                {
                    'user': user,
                    'posts': posts,
                    'category': category,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Новые статьи в категории "{category.name}" за неделю',
                body='',
                from_email='tanyamars16@yandex.ru',
                to=[user.email],
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


@shared_task
def send_post_notification(post_id):
    from .models import Post
    try:
        post = Post.objects.get(pk=post_id)
        categories = post.categories.all()
        subscribers = set()
        for category in categories:
            subscribers.update(category.subscribers.all())

        for user in subscribers:
            html_content = render_to_string(
                'email_notification.html',
                {'post': post, 'username': user.username}
            )
            msg = EmailMultiAlternatives(
                subject=post.title,
                body='',
                from_email='tanyamars16@yandex.ru',
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    except Post.DoesNotExist:
        pass
