from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView

from .models import Profile
from .forms import ProfileForm


def profile(request, username):
    user = get_object_or_404(User, username=username)
    try:
        user.profile  # Accessing a non-existent profile (they do no exist by default) triggers an error
    except Profile.DoesNotExist:
        Profile.objects.create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and request.user == user:
            skills, picture = form.cleaned_data['skills'], form.cleaned_data['picture']
            user.profile.skills.set(skills)
            user.profile.picture = picture
            user.profile.save()

            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))

    return render(request, 'user_profile/profile.html', {'profile': user.profile, 'form': ProfileForm()})


class ProfileView(DetailView):
    model = Profile
    pk_url_kwarg = 'username'
    template_name = 'user_profile/profile.html'

    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        # Accessing a non-existent profile (they do no exist by default) triggers an error
        try:
            user.profile
        except Profile.DoesNotExist:
            Profile.objects.create(user=user)
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username']).profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfileForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_object_or_404(User, username=kwargs['username'])
            if request.user == user:
                user.profile.skills.set(form.cleaned_data['skills'])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
