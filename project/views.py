import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from project.models import Project
from project.forms import ProjectForm


class CreateProjectView(PermissionRequiredMixin, CreateView):
    redirect_field_name = '/'
    permission_required = 'project.add_project'
    model = Project
    form_class = ProjectForm

    # ensures that the user who created the project is set as its manager, also adds them to the members field
    def form_valid(self, form):
        project = form.save(commit=False)
        project.manager = self.request.user
        project.save()
        project.members.add(self.request.user)
        return HttpResponseRedirect(reverse('project', kwargs={'pk': project.pk}))


class EditProjectView(UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    redirect_field_name = '/'

    def test_func(self):
        return self.request.user == get_object_or_404(Project, pk=self.kwargs['pk']).manager \
                or self.request.user.has_perm('change_project')


class DeleteProjectView(UserPassesTestMixin, DeleteView):
    model = Project
    redirect_field_name = '/'
    success_url = reverse_lazy('project_list')

    # Should be same the same in DeleteProject and EditProject
    def test_func(self):
        return self.request.user == get_object_or_404(Project, pk=self.kwargs['pk']).manager \
                or self.request.user.has_perm('delete_project')


class ProjectAdminDetailView(UserPassesTestMixin, DetailView):
    model = Project

    def test_func(self):
        return self.request.user == self.object.manager

##############################################


def apply_to_project(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user.username)
        project = get_object_or_404(Project, pk=pk)

        # if not rejected, already an applicant or already a member
        if project.applicants.filter(username=user.username).exists() or \
                project.rejected_applicants.filter(username=user.username).exists() or \
                project.members.filter(username=user.username).exists():
            return HttpResponse("You have already applied to this project")
        try:
            if project.application_end < datetime.date.today():
                return HttpResponse("Applications have ended for this project")
        except TypeError:
            return HttpResponse("This project does not have an application date set")

        project.applicants.add(user)
        project.save()
        if project.form_link:
            return HttpResponseRedirect(project.form_link)

        messages.success(request, 'You have successfully applied to ' + str(project))
        return HttpResponseRedirect(reverse('project', kwargs={'pk': pk}))
    return HttpResponseRedirect('/')


def manage_applicant(request, pk, username, accept):
    project = get_object_or_404(Project, pk=pk)
    user = get_object_or_404(User, username=username)
    if request.method == 'POST' and project.manager == request.user:
        project.applicants.remove(user)
        if accept:
            project.members.add(user)
        else:
            project.rejected_applicants.add(user)
        return HttpResponseRedirect(reverse('project_admin', kwargs={'pk': pk}))

    return PermissionDenied()


def accept_applicant(request, pk, username):
    return manage_applicant(request, pk, username, True)


def reject_applicant(request, pk, username):
    return manage_applicant(request, pk, username, False)
