from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, DeleteView

from concurrency.views import ConcurrentUpdate
from news.forms import EventForm
from news.models import Article, Event


class ArticleView(DetailView):
    model = Article
    template_name = 'news/article.html'


class ArticleList(ListView):
    queryset = Article.objects.filter(event=None)
    template_name = 'news/articles.html'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = Article
    template_name = 'news/article_create.html'
    fields = ('title', 'ingress', 'content')
    success_url = reverse_lazy('articles')
    permission_required = (
        'news.add_article'
    )


class ArticleUpdate(PermissionRequiredMixin, ConcurrentUpdate):
    model = Article
    template_name = 'news/article_update.html'
    fields = ('title', 'ingress', 'content')
    success_url = reverse_lazy('articles')
    permission_required = (
        'news.change_article'
    )


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('articles')
    permission_required = (
        'news.delete_article',
    )


class EventView(DetailView):
    model = Event
    template_name = 'news/event.html'


class EventList(ListView):
    queryset = Event.objects.filter(published=True)
    template_name = 'news/events.html'


class DraftList(ListView):
    queryset = Event.objects.filter(published=False)
    template_name = 'news/drafts.html'


class EventCreate(PermissionRequiredMixin, CreateView):
    model = Event
    template_name = 'news/article_create.html'
    form_class = EventForm
    success_url = reverse_lazy('events')
    permission_required = (
        'news.add_event'
    )


class EventUpdate(PermissionRequiredMixin, ConcurrentUpdate):
    model = Event
    template_name = 'news/article_update.html'
    fields = ('title', 'ingress', 'content', 'start_date', 'start_time', 'end_date', 'end_time', 'location',
              'location_url', 'signup_url', 'facebook_url')
    success_url = reverse_lazy('events')
    permission_required = (
        'news.change_event'
    )


class EventDelete(PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('events')
    permission_required = (
        'news.delete_event',
    )
