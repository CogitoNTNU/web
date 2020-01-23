from itertools import chain

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, DeleteView
from concurrency.views import ConcurrentUpdate
from news.forms import EventForm, ArticleCreateForm
from news.helpers import generate_mazemap_embed
from news.models import Article, Event, ArticleFile
from django import forms


class ArticleView(DetailView):
    model = Article
    template_name = 'news/article.html'


class ArticleList(ListView):
    queryset = Article.objects.filter(event=None, published=True)
    template_name = 'news/articles.html'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'news/article_create.html'
    success_url = '/'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['files'] = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
        return form

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if form.is_valid(): 
            self.object = form.save()
            for file in files:
                ArticleFile.objects.create(file=file, page=self.object)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


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
