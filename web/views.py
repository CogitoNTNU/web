from django.utils import timezone
from django.views.generic import ListView

from news.models import Event, Article


class Home(ListView):
    queryset = Article.objects.filter(published=True)\
        .exclude(id__in=Event.objects.filter(end_date__lt=timezone.now()))\
        .order_by('-datetime_published')
    template_name = 'web/index.html'
