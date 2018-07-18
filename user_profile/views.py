import datetime

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from .models import Profile, Skill, Project
from .forms import ProfileForm, ProjectForm


class DetailSkillView(DetailView):
    model = Skill


class DetailProjectView(DetailView):
    model = Project


class ListProjectView(ListView):
    model = Project


class CreateProjectView(PermissionRequiredMixin, CreateView):
    redirect_field_name = '/'
    permission_required = 'user_profile.add_project'
    model = Project
    form_class = ProjectForm


class EditProjectView(UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    redirect_field_name = '/'

    def test_func(self):
        return self.request.user == get_object_or_404(Project, pk=self.kwargs['pk']).manager


class DeleteProjectView(UserPassesTestMixin, DeleteView):
    model = Project
    redirect_field_name = '/'
    success_url = reverse_lazy('project_list')

    # Should be same the same in DeleteProject and EditProject
    def test_func(self):
        return self.request.user == get_object_or_404(Project, pk=self.kwargs['pk']).manager

##############################################


def administrate_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user == project.manager:
        return HttpResponseRedirect("/")

    return render(request, 'user_profile/project_admin.html', {'project': project})


def accept_applicant(request, pk, username):
    return manage_applicant(request, pk, username, True)


def reject_applicant(request, pk, username):
    return manage_applicant(request, pk, username, False)


def apply_to_project(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user.username)
        project = get_object_or_404(Project, pk=pk)

        # if not rejected, already an applicant or already a member
        if user in project.applicants.all() or \
                user in project.members.all() or\
                user in project.rejected_applicants.all():
            return HttpResponse("You have already applied to this project")
        try:
            if project.application_end < datetime.date.today():
                return HttpResponse("Applications have ended for this project")
        except TypeError:
            return HttpResponse("This project does not have an application date set")

        project.applicants.add(user)
        project.save()
        messages.success(request, 'You have successfully applied to ' + str(project))
        return HttpResponseRedirect(reverse('project', kwargs={'pk': pk}))

    return HttpResponseRedirect('/')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    try:
        user.profile  # Accessing a non-existent profile (they do no exist by default) triggers an error
    except Profile.DoesNotExist:
        new_profile = Profile(user=user)
        new_profile.save()

    # populate()
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # user.profile.skills.remove(user.profile.skills.all()) seems to delete all skills completely from the DB
            # removing the connection one way does not remove it the other way...?
            for skill in Skill.objects.all():
                user.profile.skills.remove(skill)
                skill.members.remove(user.profile)
            for skill in form.cleaned_data['skills']:
                user.profile.skills.add(skill)
                skill.members.add(user.profile)
            user.profile.picture.delete()
            user.profile.picture = form.cleaned_data['picture']
            user.profile.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))

    return render(
        request,
        'user_profile/profile.html',
        {'profile': user.profile, 'edit': request.user == user, 'form': form}
    )


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

    else:
        return HttpResponse("Something went wrong")

