import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from project.models import Project, Collection
from project.forms import ProjectForm


class CreateCollectionView(PermissionRequiredMixin, CreateView):
    permission_required = 'project.add_collection'
    model = Collection
    fields = ('name', 'description', 'form_link', 'application_end_date',)
    redirect_field_name = '/'


class CreateProjectView(PermissionRequiredMixin, CreateView):
    permission_required = 'project.add_project'
    model = Project
    form_class = ProjectForm

    # ensures that the user who created the project is set as its manager, also adds them to the members field
    def form_valid(self, form, **kwargs):
        project = form.save(commit=False)

        project.manager = self.request.user
        project.save()
        project.members.add(self.request.user)
        project.collection.applicants.add(self.request.user)
        return HttpResponseRedirect(reverse('project', kwargs={'pk': project.pk}))


class EditProjectView(UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    redirect_field_name = '/'

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())

        # remove application_end field, as it is only to be used on project creation
        form.fields.pop('application_end', None)
        return form

    def test_func(self):
        return self.request.user == get_object_or_404(Project, pk=self.kwargs['pk']).manager \
                or self.request.user.has_perm('change_project')


class DeleteProjectView(UserPassesTestMixin, DeleteView):
    model = Project
    redirect_field_name = '/'
    success_url = reverse_lazy('collection_list')

    # Should be same the same in DeleteProject and EditProject
    def test_func(self):
        return self.request.user == get_object_or_404(Project, pk=self.kwargs['pk']).manager \
                or self.request.user.has_perm('delete_project')


class ProjectAdminDetailView(UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'project/project_admin.html'

    def test_func(self):
        return self.request.user == self.get_object().manager

##############################################


def apply_to_collection(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user.username)
        collection = get_object_or_404(Collection, pk=pk)

        if collection.applicants.filter(username=user.username).exists():
            return HttpResponse("You have already applied to this project")
        try:
            if not collection.application_open:
                return HttpResponse("Applications have ended for this project")
        except TypeError:
            return HttpResponse("This project does not have an application date set")

        collection.applicants.add(user)
        collection.save()
        if collection.form_link:
            return HttpResponseRedirect(collection.form_link)

        messages.success(request, 'You have successfully applied to ' + str(collection))
        return HttpResponseRedirect(reverse('project', kwargs={'pk': pk}))
    return HttpResponseRedirect('/')


def manage_applicant(request, pk, username, accept):
    project = get_object_or_404(Project, pk=pk)
    user = get_object_or_404(User, username=username)
    if request.method == 'POST' and request.user == project.manager:
        if accept:
            project.members.add(user)
        else:
            project.rejected_applicants.add(user)
        return HttpResponseRedirect(reverse('project_admin', kwargs={'pk': pk}))

    return PermissionDenied()


def accept_applicant(request, pk, username):
    return manage_applicant(request, pk, username, accept=True)


def reject_applicant(request, pk, username):
    return manage_applicant(request, pk, username, accept=False)
