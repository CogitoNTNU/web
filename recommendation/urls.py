from django.conf.urls import url
from django.urls import path
from .views import CreateEntryView, DeleteEntryView, \
    EditEntryView, view_entry, CreateTagView, ListEntriesView

urlpatterns = [
    path('create/', CreateEntryView.as_view(), name="entry_form"),
    path('edit/<int:pk>/', EditEntryView.as_view(), name="edit_entry"),
    path('delete/<int:pk>/', DeleteEntryView.as_view(), name="delete_entry"),
    path('detail/<int:pk>/', view_entry, name="entry_detail"),
    path('tag/add/', CreateTagView.as_view(), name="tag_form"),
    path('/', ListEntriesView.as_view(), name="entry_list"),
]
