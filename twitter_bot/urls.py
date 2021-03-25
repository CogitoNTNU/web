from . import views
from django.urls import path, re_path
from twitter_bot.views import like_tweet
from twitter_bot.models import Tweet

urlpatterns = [
    path('', views.TweetList.as_view(), name='tweets'),
    path('like_tweet/<pk>', views.like_tweet, name='like-tweet')
]
