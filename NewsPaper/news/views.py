from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'  # шаблон для отображения конкретной новости
    context_object_name = 'news'
