from django.urls import path
from .views import (
    NewsList, NewsDetail, NewsCreate, ArticleCreate,
    NewsUpdate, ArticleUpdate, NewsDelete, ArticleDelete, NewsSearch, become_author, subscribe_to_category
)


urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='news_delete'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('become_author/', become_author, name = 'become_author'),
    path('subscribe/<int:category_id>/', subscribe_to_category, name='subscribe'),

]