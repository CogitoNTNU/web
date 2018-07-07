from pprint import pprint

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from .helpers import get_related_entries, get_entry_tags
from .forms import EntryForm, TagForm
from .models import Entry, Tag


class ListEntriesView(ListView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.all().order_by('-creation_date')  # minus-sign => descending order


class CreateEntryView(PermissionRequiredMixin, CreateView):
    permission_required = 'recommendation.add_entry'
    redirect_field_name = 'recommend/entry_detail.html'
    form_class = EntryForm
    model = Entry


class DeleteEntryView(PermissionRequiredMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy('entry_list')
    permission_required = 'recommendation.delete_entry'


class EditEntryView(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'recommend/entry_detail.html'
    permission_required = 'recommendation.change_entry'
    success_url = reverse_lazy('entry_list')
    model = Entry
    form_class = EntryForm


class DetailEntryView(DetailView):
    model = Entry


class CreateTagView(PermissionRequiredMixin, CreateView):
    permission_required = 'recommendation.add_tag'
    redirect_field_name = 'recommend/entry_list.html'
    form_class = TagForm
    model = Tag
    success_url = '/recommend/tag/add/'


###########################################################
###########################################################

def view_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    related_entries = get_related_entries(entry)[:4]
    return render(request,
                  'recommendation/entry_detail.html',
                  context={'entry': entry, 'related': related_entries, 'tags': get_entry_tags(entry)})
