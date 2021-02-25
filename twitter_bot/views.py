from django.shortcuts import render
from django.views import generic
from .models import Tweet
from django.core.exceptions import ObjectDoesNotExist
import json


class TweetList(generic.ListView):
    model = Tweet
    template_name = 'tweet_list.html'
    paginate_by = 10

    def get_queryset(self):
        Tweet = self.model.objects.all()
        return Tweet


try:
    go = Tweet.objects.all()[:1].get()
except ObjectDoesNotExist:
    with open("twitter_bot/templates/tweets.json") as f:
        p = 0
        data = json.load(f)
        d = {}
        for i in data['tweets']:
            d["Tweet{}".format(p)] = Tweet.objects.create(content=i, tweet_id=p)
            p += 1

