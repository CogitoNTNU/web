from django import forms
from django.db import OperationalError

from .models import Profile, Skill, Project


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('skills', 'projects')

        try:
            widgets = {  # The first object in the tuple is the external representation, the second the internal
                'skills': forms.SelectMultiple(choices=[(str(obj), obj) for obj in Skill.objects.all()],
                                               attrs={'class': 'ui multiple search selection dropdown'})
            }
        except OperationalError:
            pass
