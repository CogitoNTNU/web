from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView

from .models import Profile, Skill
from .forms import ProfileForm


class DetailSkillView(DetailView):
    model = Skill

##############################################


def profile(request, username):
    user = get_object_or_404(User, username=username)
    try:
        user.profile  # Accessing a non-existent profile (they do no exist by default) triggers an error
    except Profile.DoesNotExist:
        Profile(user=user)

    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.profile.skills = form.cleaned_data['skills']
            # return HttpResponseRedirect(reverse('user_profile:profile', kwargs={'username': username}))

    return render(
        request,
        'user_profile/profile.html',
        {'profile': user.profile, 'edit': request.user == user, 'form': form}
    )

