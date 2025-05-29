from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import get_object_or_404, redirect
from django_filters.views import FilterView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from .tasks import send_post_notification


class NewsList(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']
    paginate_by = 10


class NewsSearch(FilterView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_list'
    filterset_class = PostFilter
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        user = self.request.user
        today = now().date()
        post_count_today = Post.objects.filter(
            author=user,
            created_at__date=today
        ).count()

        if post_count_today >= 3:
            messages.error(self.request, 'Вы не можете создавать более 3 публикаций в сутки.')
            return self.form_invalid(form)

        form.instance.publication_type = 'NW'
        form.instance.author = self.request.user
        response = super().form_valid(form)
        send_post_notification.delay(form.instance.pk)
        return response


class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        user = self.request.user
        today = now().date()
        post_count_today = Post.objects.filter(
            author=user,
            created_at__date=today
        ).count()

        if post_count_today >= 3:
            messages.error(self.request, 'Вы не можете создавать более 3 публикаций в сутки.')
            return self.form_invalid(form)

        form.instance.publication_type = 'AR'
        form.instance.author = self.request.user
        response = super().form_valid(form)
        send_post_notification.delay(form.instance.pk)
        return response


class NewsUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class ArticleUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class NewsDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.delete_post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class ArticleDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.delete_post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


@login_required
def become_author(request):
    user = request.user
    author_group, created = Group.objects.get_or_create(name='authors')
    if not user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('news_list')


@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))
