from itertools import chain

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, DeleteView
from concurrency.views import ConcurrentUpdate
from news.forms import EventForm, ArticleCreateForm
from news.helpers import generate_mazemap_embed
from news.models import Article, Event, ArticleFile
from django import forms
from django.shortcuts import redirect


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
    permission_required = 'news.add_article'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['files'] = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
        return form

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        self.object = form.save()
        if form.is_valid(): 
            for file in files:
                ArticleFile.objects.create(file=file, article=self.object)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ArticleUpdate(PermissionRequiredMixin, ConcurrentUpdate):
    model = Article
    template_name = 'news/article_update.html'
    form_class = ArticleCreateForm
    permission_required = 'news.change_article'
    success_url = '/news/articles/'

    def get_form(self, form_class=None, **kwargs):
        form = super().get_form()
        form.request = self.request
        self.object = self.get_object() 
        article = Article.objects.get(pk = self.kwargs['pk'])
        form.fields['files'] = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
        for file in ArticleFile.objects.filter(article = article):
            form.fields[file.filename] = forms.BooleanField(widget=forms.CheckboxInput, required=False, label='Delete previously uploaded file [' + file.filename + ']?'
            )
        return form

    def post(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission_required):
            form_class = super().get_form_class()
            form = self.get_form(form_class)
            files = request.FILES.getlist('files')
            article = Article.objects.get(pk = self.kwargs['pk'])
            form.is_valid()
            print(form.cleaned_data)
            if form.is_valid():
                for deletefile in ArticleFile.objects.filter(article = article):
                    if form.cleaned_data.pop(deletefile.filename, False):
                        deletefile.delete()
                for file in files:
                    ArticleFile.objects.create(file=file, article=self.get_object())
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        
    def form_valid(self, form_class):   
        article = self.get_object()
        article.title = form_class.cleaned_data['title']
        article.ingress = form_class.cleaned_data['ingress']
        article.content = form_class.cleaned_data['content']
        article.banner = form_class.cleaned_data['banner']
        article.published = form_class.cleaned_data['published']
        article.pinned = form_class.cleaned_data['pinned']  
        article.save()
        return redirect(self.success_url)

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


class EventCreate(ArticleCreate):
    model = Event
    form_class = EventForm
    template_name = 'news/article_create.html'
    success_url = '/'
    permission_required = 'news.add_event'


class EventUpdate(ArticleUpdate):
    model = Event
    form_class = EventForm
    template_name = 'news/article_update.html'
    permission_required = 'news.change_event'
    success_url = '/news/events/'


class EventDelete(PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'web/confirm_delete.html'
    success_url = reverse_lazy('events')
    permission_required = (
        'news.delete_event',
    )
