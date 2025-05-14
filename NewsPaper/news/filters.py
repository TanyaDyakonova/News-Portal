import django_filters
from django import forms
from .models import Post, Category
from .resources import PUBLICATION_CHOICES


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Название'
    )
    publication_type = django_filters.ChoiceFilter(
        field_name='publication_type',
        choices=PUBLICATION_CHOICES,
        label='Тип публикаций'
    )

    categories = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория'
    )
    created_at = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата позже'
    )

    class Meta:
        model = Post
        fields = ['title', 'categories', 'created_at', 'publication_type']