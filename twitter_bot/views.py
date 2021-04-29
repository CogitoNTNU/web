from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Tweet
from django.core.exceptions import ObjectDoesNotExist
import json
from django.db.models import F
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect


class TweetList(generic.ListView):
    model = Tweet
    template_name = 'tweet_list.html'
    paginate_by = 4

    def get_queryset(self):
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

        tweet = self.model.objects.all()
        return tweet


@csrf_exempt
def like_tweet(request, pk):
    tweet = Tweet.objects.get(pk=pk)
    tweet.likes += 1
    tweet.save()
    print('dank')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

