from django.urls import path
from .models import Resource
from django.views.generic import ListView

from .views import CreateResourceView, DeleteResourceView, \
    EditResourceView, view_resource, CreateTagView

urlpatterns = [
    path('create/', CreateResourceView.as_view(), name="resource_form"),
    path('<int:pk>/edit/', EditResourceView.as_view(), name="edit_resource"),
    path('<int:pk>/delete/', DeleteResourceView.as_view(), name="delete_resource"),
    path('<int:pk>/', view_resource, name="resource_detail"),
    path('tag/add/', CreateTagView.as_view(), name="tag_form"),
    path('', ListView.as_view(model=Resource), name="resource_list"),
]
