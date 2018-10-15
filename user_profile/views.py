from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Profile, Skill
from .forms import ProfileForm


def profile(request, username):
    user = get_object_or_404(User, username=username)
    try:
        user.profile  # Accessing a non-existent profile (they do no exist by default) triggers an error
    except Profile.DoesNotExist:
        Profile.objects.create(user=user)

    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and request.user == user:
            # removing the connection one way does not remove it the other way...?
            user.profile.skills.clear()
            for skill in Skill.objects.all():
                skill.members.remove(user.profile)
            for skill in form.cleaned_data['skills']:
                user.profile.skills.add(skill)
                skill.members.add(user.profile)
            """
            user.profile.picture.delete()
            user.profile.picture = form.cleaned_data['picture']
            user.profile.save()
            """
            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))

    return render(
        request,
        'user_profile/profile.html',
        {'profile': user.profile, 'edit': request.user == user, 'form': form}
    )

