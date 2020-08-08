from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from verv.models import Verv, VervGroup
from verv.forms import VervForm


class CreateVervGroupView(PermissionRequiredMixin, CreateView):
    permission_required = 'verv.add_vervgroup'
    model = VervGroup
    fields = ('name', 'description', 'form_link', 'application_end_date',)
    redirect_field_name = '/'


class CreateVervView(PermissionRequiredMixin, CreateView):
    permission_required = 'verv.add_verv'
    model = Verv
    form_class = VervForm

    # ensures that the user who created the verv is set as its manager, also adds them to the members field
    def form_valid(self, form, **kwargs):
        verv = form.save(commit=False)   
        verv.save()
        return HttpResponseRedirect(reverse('verv', kwargs={'pk': verv.pk}))


class EditVervView(PermissionRequiredMixin, UpdateView):
    permission_required = 'verv.change_verv'
    model = Verv
    form_class = VervForm
    redirect_field_name = '/'
    success_url = reverse_lazy('vervgroup_list')


class DeleteVervView(PermissionRequiredMixin, DeleteView):
    permission_required = 'verv.delete_verv'
    model = Verv
    redirect_field_name = '/'
    template_name = 'web/confirm_delete.html'
    success_url = reverse_lazy('vervgroup_list')


