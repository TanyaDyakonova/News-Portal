from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'categories']

        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'author': 'Автор',
            'categories': 'Категории',
        }
