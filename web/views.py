from datetime import datetime
from pytz import timezone

from django.shortcuts import render
from django.views.generic import ListView

from news.models import Event, Article
from project.models import Project
from uptake.models import Uptake
from itertools import chain


def sort_events_articles(o):
    """ :param o: article or event object
        :return: tuple:
            pinned: yes/no
            datetime by which they should be sorted. start-datetime for events. created-datetime for articles"""
    cet = timezone("Europe/Oslo")
    if o.__class__.__name__ == "Event":
        return o.pinned, datetime.combine(o.start_date, o.start_time, tzinfo=cet)
    else:  # => Article
        return o.pinned, o.datetime_created


class Home(ListView):
    template_name = 'web/indexc.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context.update({'projects': Project.objects.all()[:4]})
        return context

    def get_queryset(self):
        articles = Article.objects.filter(published=True).exclude(id__in=Event.objects.all())
        events = Event.objects.filter(published=True)
        uptakes = Uptake.objects.all()
        feed = sorted(chain(articles, events), key=sort_events_articles, reverse=True)
        return list(uptakes) + feed 


    
def handler404(request, *args, **argv):
    return render(request, 'web/404.html', status=404)
