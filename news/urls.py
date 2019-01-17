from django.urls import path

from news.views import ArticleUpdate, ArticleView, ArticleCreate, ArticleList, ArticleDelete, EventList, EventCreate, \
    EventDelete, EventUpdate, EventView, DraftList

urlpatterns = [
    path('article/<int:pk>/', ArticleView.as_view(), name='article'),
    path('articles/', ArticleList.as_view(), name='articles'),
    path('article/new/', ArticleCreate.as_view(), name='article-create'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article-delete'),
    path('event/<int:pk>/', EventView.as_view(), name='event'),
    path('events/', EventList.as_view(), name='events'),
    path('event/new/', EventCreate.as_view(), name='event-create'),
    path('event/<int:pk>/update/', EventUpdate.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', EventDelete.as_view(), name='event-delete'),
    path('events/drafts/', DraftList.as_view(), name='drafts')
]
