from django.utils import timezone
from django.views.generic import ListView

from news.models import Event, Article
from itertools import chain



class Home(ListView):
    """
    queryset = Article.objects.filter(published=True)\
        .exclude(id__in=Event.objects.filter(end_date__lt=timezone.now()))\
        .order_by('-datetime_published')
    """
    queryset = Article.objects.filter(published=True).exclude(id__in=Event.objects.all())
    #events = Event.objects.filter(end_date__gt=timezone.now())
    #queryset = sorted(chain(articles, events), key=lambda o: o.datetime_published)
    template_name = 'web/index.html'
