from itertools import chain

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, DeleteView
from concurrency.views import ConcurrentUpdate
from news.forms import EventForm
from news.helpers import generate_mazemap_embed
from news.models import Article, Event


class ArticleView(DetailView):
    model = Article
    template_name = 'news/article.html'


class ArticleList(ListView):
    queryset = Article.objects.filter(event=None, published=True)
    template_name = 'news/articles.html'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'ingress', 'content', 'published', 'banner')
    template_name = 'news/article_create.html'
    success_url = '/'
    permission_required = 'news.add_article'


class ArticleUpdate(PermissionRequiredMixin, ConcurrentUpdate):
    model = Article
    template_name = 'news/article_update.html'
    fields = ArticleCreate.fields
    success_url = '/'
    permission_required = 'news.change_article'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = 'web/confirm_delete.html'
    success_url = reverse_lazy('articles')
    permission_required = 'news.delete_article'


class EventView(DetailView):
    model = Event
    template_name = 'news/event.html'


class EventList(ListView):
    queryset = Event.objects.filter(published=True)
    template_name = 'news/events.html'


class DraftList(ListView):
    template_name = 'news/drafts.html'

    def get_queryset(self):
        articles = Article.objects.filter(published=False).exclude(id__in=Event.objects.all())
        events = Event.objects.filter(published=False)
        return list(reversed(sorted(chain(articles, events), key=lambda o: o.datetime_created)))


class EventCreate(PermissionRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'news/article_create.html'
    success_url = '/'
    permission_required = 'news.add_event'


class EventUpdate(PermissionRequiredMixin, ConcurrentUpdate):
    model = Event
    form_class = EventForm
    template_name = 'news/article_update.html'
    permission_required = 'news.change_event'
    success_url = '/'


class EventDelete(PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'web/confirm_delete.html'
    success_url = reverse_lazy('events')
    permission_required = (
        'news.delete_event',
    )
