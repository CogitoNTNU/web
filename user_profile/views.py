from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from .models import Profile


##############################################

def profile(request, username):
    user = get_object_or_404(User, username=username)
    try:
        profile = user.profile
        return render(request, 'user_profile/profile.html', {'profile': profile, 'edit': request.user == user})
    except Profile.DoesNotExist:
        Profile(user=user)
        return render(request, 'user_profile/profile.html', {'profile': user.profile, 'edit': request.user == user})

