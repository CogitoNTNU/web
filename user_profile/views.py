from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView

from .models import Profile, Skill, Project
from .forms import ProfileForm


class DetailSkillView(DetailView):
    model = Skill

##############################################


def profile(request, username):
    user = get_object_or_404(User, username=username)
    try:
        user.profile  # Accessing a non-existent profile (they do no exist by default) triggers an error
    except Profile.DoesNotExist:
        new_profile = Profile(user=user)
        new_profile.save()

    populate()
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            for skill in form.cleaned_data['skills']:
                user.profile.skills.add(skill)
            # return HttpResponseRedirect(reverse('user_profile:profile', kwargs={'username': username}))

    return render(
        request,
        'user_profile/profile.html',
        {'profile': user.profile, 'edit': request.user == user, 'form': form}
    )


def populate():
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

