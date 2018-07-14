from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
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
    permission_required = 'user_profile.add_entry'
    model = Project
    form_class = ProjectForm


class EditProjectView(UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    permission_required = 'user_profile.change_project'
    redirect_field_name = '/'

    def test_func(self):
        return self.request.user == get_object_or_404(Project, pk=self.kwargs['pk']).manager


class DeleteProjectView(UserPassesTestMixin, DeleteView):
    model = Project
    permission_required = 'user_profile.delete_project'
    redirect_field_name = '/'
    success_url = reverse_lazy('/')

    # Should be same the same in DeleteProject and EditProject
    def test_func(self, user, project):
        return self.request.user == get_object_or_404(Project, pk=self.kwargs['pk']).manager



##############################################


def apply_to_project(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user.username)
        project = get_object_or_404(Project, pk=pk)

        # if not rejected, already an applicant or already a member
        if user in project.applicants.all():
            return HttpResponse("You have already applied to this project")

        project.applicants.add(user)
        project.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'pk': pk}))


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
            user.profile.picture = form.cleaned_data['picture']
            user.profile.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))

    return render(
        request,
        'user_profile/profile.html',
        {'profile': user.profile, 'edit': request.user == user, 'form': form}
    )


def populate():
    print("POPULATING...")
    print(".")
    print(".")
    s1 = Skill(name='ku')
    s2 = Skill(name='hest')
    s3 = Skill(name='gris')

    for s in [s1, s2, s3]:
        s.save()

    p1 = Project(title='Nytt hus')
    p2 = Project(title='Male båt')
    p1.save()
    p2.save()

    u1 = User(username='Pål', password='123qweasd')
    u2 = User(username='Gunnar', password='123qweasd')
    u1.save()
    u2.save()

    p1 = Profile(user=u1)
    p2 = Profile(user=u2)
    p1.skills.add(s1)
    p1.skills.add(s2)
    p2.skills.add(s2)
    p2.skills.add(s3)
    p1.projects.add(p1)
    p2.projects.add(p1)
    p2.projects.add(p2)
    p1.save()
    p2.save()
    print("DONE")
