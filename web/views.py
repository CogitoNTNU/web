from django.utils import timezone
from django.views.generic import ListView

from news.models import Event


class Home(ListView):
    queryset = Event.objects.filter(start_date__gte=timezone.now())
    template_name = 'web/index.html'
