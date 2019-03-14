from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView

from news.models import Event, Article
from itertools import chain


def sort_events_articles_sticky(o):
    return o.sticky


def sort_events_articles(o):
    # Note: does not account for time, only dates.
    # events occurring on the same date and articles published on the same date will
    # possibly appear in the wrong order
    try:
        return o.start_date
    except AttributeError:
        return o.datetime_created.date()


class Home(ListView):
    template_name = 'web/index.html'
    paginate_by = 6

    def get_queryset(self):
        articles = Article.objects.filter(published=True).exclude(id__in=Event.objects.all())
        events = Event.objects.filter(published=True)
        return list(reversed(sorted(sorted(chain(articles, events), key=sort_events_articles), key=sort_events_articles_sticky)))


def handler404(request, *args, **argv):
    return render(request, 'web/404.html', status=404)
