from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from .models import Profile


class ProfileDetailView(DetailView):
    model = Profile

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


##############################################

def specific_profile(request, username):
    user = get_object_or_404(User, username=username)
    try:
        profile = user.profile
        return render(request, 'user_profile/profile.html', {'profile': profile})
    except Profile.DoesNotExist:
        Profile(user=user)
        return render(request, 'user_profile/profile.html', {'profile': user.profile})


def self_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.user.is_authenticated:
        return render(request, 'user_profile/profile.html', {'profile': profile})

