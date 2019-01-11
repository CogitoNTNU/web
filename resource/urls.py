from django.urls import path
from .models import Resource
from django.views.generic import ListView

from .views import ResourceCreateView, ResourceChangeView, \
    ResourceUpdateView, view_resource, TagCreateView, add_remove_starred

urlpatterns = [
    path('create/', ResourceCreateView.as_view(), name="resource_form"),
    path('<int:pk>/edit/', ResourceUpdateView.as_view(), name="edit_resource"),
    path('<int:pk>/delete/', ResourceChangeView.as_view(), name="delete_resource"),
    path('<int:pk>/', view_resource, name="resource_detail"),
    path('tag/add/', TagCreateView.as_view(), name="tag_form"),
    path('', ListView.as_view(model=Resource, paginate_by=10), name="resource_list"),

    path('star/', add_remove_starred, name="star"),
]
