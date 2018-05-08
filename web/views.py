from django.views.generic import ListView

from news.models import Article


class Home(ListView):
    model = Article
    template_name = 'web/index.html'
