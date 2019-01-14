from django.urls import path
from django.views.generic import DetailView

from single_page.models import SinglePage
from single_page.views import SinglePageCreateView, SinglePageChangeView, SinglePageDeleteView

urlpatterns = [
    path('single_page/create', SinglePageCreateView.as_view(), name='create_single_page'),
    path('<slug:url>/change', SinglePageChangeView.as_view(), name='change_single_page'),
    path('<slug:url>/delete', SinglePageDeleteView.as_view(), name='delete_single_page'),
    path('<str:slug>/', DetailView.as_view(model=SinglePage), name='single_page'),
]
