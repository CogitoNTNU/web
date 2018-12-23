from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.contrib import messages

from .helpers import get_related_resources
from .forms import ResourceForm, TagForm
from .models import Resource, Tag


class ResourceCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'resource.add_resource'
    redirect_field_name = 'recommend/resource_detail.html'
    form_class = ResourceForm
    model = Resource


class ResourceChangeView(PermissionRequiredMixin, DeleteView):
    model = Resource
    success_url = reverse_lazy('resource_list')
    permission_required = 'resource.delete_resource'


class ResourceUpdateView(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'recommend/resource_detail.html'
    permission_required = 'resource.change_resource'
    model = Resource
    form_class = ResourceForm


class TagCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'resource.add_tag'
    redirect_field_name = 'recommend/resource_list.html'
    model = Tag
    form_class = TagForm
    success_url = '/resources/tag/add/'
    success_message = '%(name)s was added successfully!'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


###########################################################
###########################################################

def view_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    related_resources = get_related_resources(resource, 4)
    return render(request,
                  'resource/resource_detail.html',
                  context={'resource': resource, 'related': related_resources, 'tags': resource.tags.all()})
