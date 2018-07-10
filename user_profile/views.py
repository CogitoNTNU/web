from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from .models import Profile


##############################################

def profile(request, username):
    user = get_object_or_404(User, username=username)
    try:
        user.profile  # Accessing a non-existent profile (they do no exist by default) triggers an error
    except Profile.DoesNotExist:
        Profile(user=user)
    return render(request, 'user_profile/profile.html', {'profile': user.profile, 'edit': request.user == user})

