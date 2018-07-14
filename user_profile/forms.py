from django import forms
from django.db import OperationalError

from .models import Profile, Skill, Project


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('picture', 'skills', )

        try:
            widgets = {  # The first object in the tuple is the external representation, the second the internal
                'skills': forms.SelectMultiple(choices=[(str(obj), obj) for obj in Skill.objects.all()],
                                               attrs={'class': 'ui multiple search selection dropdown'}),
            }
        except OperationalError:
            pass


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('title', 'description', 'application_end', )

        widgets = {
            'application_end': forms.DateInput(attrs={'type': 'date'})
        }
