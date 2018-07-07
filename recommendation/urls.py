from django.conf.urls import url
from .views import CreateEntryView, DeleteEntryView, \
    EditEntryView, view_entry, CreateTagView, ListEntriesView

urlpatterns = [
    url(r'^$', ListEntriesView.as_view(), name="entry_list"),
    url(r'^create/$', CreateEntryView.as_view(), name="entry_form"),
    url(r'^edit/(?P<pk>\d+)/$', EditEntryView.as_view(), name="edit_entry"),
    url(r'^delete/(?P<pk>\d+)/$', DeleteEntryView.as_view(), name="delete_entry"),
    url(r'^detail/(?P<pk>\d+)/$', view_entry, name="entry_detail"),
    url(r'^tag/add/$', CreateTagView.as_view(), name="tag_form"),
]
