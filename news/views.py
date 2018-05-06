from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, DeleteView

from concurrency.views import ConcurrentUpdate
from news.models import Article


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('articles')
    permission_required = (
        'news.delete_article',
    )


class ArticleList(ListView):
    model = Article
    template_name = 'news/articles.html'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = Article
    template_name = 'news/article_create.html'
    fields = ('title', 'content')
    success_url = reverse_lazy('articles')
    permission_required = (
        'news.add_article'
    )


class ArticleUpdate(PermissionRequiredMixin, ConcurrentUpdate):
    model = Article
    template_name = 'news/article_update.html'
    fields = ('title', 'content')
    success_url = reverse_lazy('articles')
    permission_required = (
        'news.change_article'
    )


class ArticleView(DetailView):
    model = Article
    template_name = 'news/article.html'
