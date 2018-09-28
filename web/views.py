from itertools import chain

from django.utils import timezone
from django.views.generic import ListView

from news.models import Event, Article


class Home(ListView):
    # queryset_event = Event.objects.filter(start_date__gte=timezone.now(), published=True)
    # queryset_article = Article.objects.filter().exclude(id__in=Event.objects.all())
    queryset = Article.objects.filter(published=True).exclude(id__in=Event.objects.filter(start_date__gte=timezone.now()))

    template_name = 'web/index.html'
