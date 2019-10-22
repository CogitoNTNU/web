from datetime import datetime
from pytz import timezone

from django.shortcuts import render
from django.views.generic import ListView

from news.models import Event, Article
from itertools import chain


def sort_events_articles_pinned(o):
    return o.pinned


def sort_events_articles(o):
    """ :param o: article or event object
        :return: datetime by which they should be sorted. start-datetime for events. created-datetime for articles"""
    cet = timezone("Europe/Oslo")
    if o.__class__.__name__ == "Event":
        return datetime.combine(o.start_date, o.start_time, tzinfo=cet)
    else:  # => Article
        return o.datetime_created


class Home(ListView):
    template_name = 'web/index.html'
    paginate_by = 6

    def get_queryset(self):
        articles = Article.objects.filter(published=True).exclude(id__in=Event.objects.all())
        events = Event.objects.filter(published=True)
        return sorted(
                    sorted(chain(articles, events), key=sort_events_articles, reverse=True),
                    key=sort_events_articles_pinned, reverse=True)


def handler404(request, *args, **argv):
    return render(request, 'web/404.html', status=404)
