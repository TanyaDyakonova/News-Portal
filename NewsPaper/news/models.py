from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .resources import PUBLICATION_CHOICES



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        post_rating = sum(post.rating for post in self.posts.all())*3
        comment_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        post_comment_rating = sum(comment.rating for post in self.posts.all() for comment in post.comments.all())
        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    publication_type = models.CharField(max_length=2, choices=PUBLICATION_CHOICES, default='AR')
    created_at=models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts')

    def __str__(self):
        return f'{self.title} ({self.get_publication_type_display()})'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + ('...' if len(self.content) > 124 else '')

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name} - {self.post.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} on {self.post.title}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



