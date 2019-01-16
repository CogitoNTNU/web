from django.urls import path
from django.views.generic import DetailView

from single_page.models import SinglePage
from single_page.views import SinglePageCreateView, SinglePageUpdateView, SinglePageDeleteView, image_view, \
    SingleImageCreateView, SingleImageDeleteView

urlpatterns = [
    path('page/create', SinglePageCreateView.as_view(), name='create_single_page'),
    path('image/create', SingleImageCreateView.as_view(), name='create_single_image'),
    path('<str:slug>/update', SinglePageUpdateView.as_view(), name='change_single_page'),
    path('<str:slug>/delete', SinglePageDeleteView.as_view(), name='delete_single_page'),
    path('<str:slug>/delete', SingleImageDeleteView.as_view(), name='delete_single_image'),
    path('<str:slug>/', DetailView.as_view(model=SinglePage), name='single_page'),
    path('i/<str:slug>/', image_view, name='single_image'),
]
