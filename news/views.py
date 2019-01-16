from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, CreateView, ListView, DeleteView

from django import forms
from concurrency.views import ConcurrentUpdate
from news.forms import EventForm
from news.models import Article, Event


class ArticleView(DetailView):
    model = Article
    template_name = 'news/article.html'


class ArticleList(ListView):
    queryset = Article.objects.filter(event=None, published=True)
    template_name = 'news/articles.html'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = Article
    template_name = 'news/article_create.html'
    fields = ('title', 'ingress', 'content', 'published',)
    success_url = reverse_lazy('articles')
    permission_required = (
        'news.add_article'
    )


class ArticleUpdate(PermissionRequiredMixin, ConcurrentUpdate):
    model = Article
    template_name = 'news/article_update.html'
    fields = ArticleCreate.fields
    success_url = reverse_lazy('articles')
    permission_required = (
        'news.change_article'
    )

    # If someone moves an article from draft to published: set published datetime to now
    def form_valid(self, form):
        article = form.save(commit=False)
        if Article.objects.get(pk=self.kwargs['pk']).published is False \
                and article.published is True:
            article.datetime_published = timezone.now()
        article.save()
        return HttpResponseRedirect(reverse_lazy('events'))


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
    queryset = Article.objects.filter(published=False)
    template_name = 'news/drafts.html'


class EventCreate(PermissionRequiredMixin, CreateView):
    model = Event
    template_name = 'news/article_create.html'
    form_class = EventForm
    success_url = reverse_lazy('events')
    permission_required = (
        'news.add_event'
    )


# Because of the implementation of ConcurrentUpdate, fields cannot be substituted with form
class EventUpdate(PermissionRequiredMixin, ConcurrentUpdate):
    model = Event
    template_name = 'news/article_update.html'
    form_class = EventForm
    permission_required = (
        'news.change_event'
    )

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            event = form.save(commit=False)
            if Event.objects.get(pk=self.kwargs['pk']).published is False \
                    and event.published is True:
                event.datetime_published = timezone.now()
            event.save()
        return super().post(request, *args, **kwargs)


class EventDelete(PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('events')
    permission_required = (
        'news.delete_event',
    )
