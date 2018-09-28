from django.utils import timezone
from django.views.generic import ListView

from news.models import Event, Article


class Home(ListView):
    queryset = Article.objects.filter(published=True)\
        .exclude(id__in=Event.objects.filter(start_date__lte=timezone.now()))
    template_name = 'web/index.html'
