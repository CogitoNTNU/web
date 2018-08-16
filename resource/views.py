from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .helpers import get_related_resources
from .forms import ResourceForm, TagForm
from .models import Resource, Tag


class CreateResourceView(PermissionRequiredMixin, CreateView):
    permission_required = 'resource.add_resource'
    redirect_field_name = 'recommend/resource_detail.html'
    form_class = ResourceForm
    model = Resource


class DeleteResourceView(PermissionRequiredMixin, DeleteView):
    model = Resource
    success_url = reverse_lazy('resource_list')
    permission_required = 'resource.delete_resource'


class EditResourceView(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'recommend/resource_detail.html'
    permission_required = 'resource.change_resource'
    model = Resource
    form_class = ResourceForm


class CreateTagView(PermissionRequiredMixin, CreateView):
    permission_required = 'resource.add_tag'
    redirect_field_name = 'recommend/resource_list.html'
    form_class = TagForm
    model = Tag
    success_url = '/recommend/tag/add/'


###########################################################
###########################################################

def view_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    related_entries = get_related_resources(resource)[:4]
    return render(request,
                  'recommendation/resource_detail.html',
                  context={'resource': resource, 'related': related_entries, 'tags': resource.tags.all()})
