from django.urls import path

from news.views import ArticleUpdate, ArticleView, ArticleCreate, ArticleList, ArticleDelete

urlpatterns = [
    path('articles/', ArticleList.as_view(), name='articles'),
    path('article/new/', ArticleCreate.as_view(), name='article-create'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article-delete'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article-update'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article'),
]
