from . import views
from django.urls import path
from twitter_bot.models import Tweet

urlpatterns = [
    path('', views.TweetList.as_view(), name='tweets'),
]