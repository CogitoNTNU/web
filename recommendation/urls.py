from django.urls import path
from .models import Entry
from django.views.generic import ListView

from .views import CreateEntryView, DeleteEntryView, \
    EditEntryView, view_entry, CreateTagView

urlpatterns = [
    path('create/', CreateEntryView.as_view(), name="entry_form"),
    path('edit/<int:pk>/', EditEntryView.as_view(), name="edit_entry"),
    path('delete/<int:pk>/', DeleteEntryView.as_view(), name="delete_entry"),
    path('detail/<int:pk>/', view_entry, name="entry_detail"),
    path('tag/add/', CreateTagView.as_view(), name="tag_form"),
    path('', ListView.as_view(model=Entry), name="entry_list"),
]
