from django import forms
from .models import Profile, Skill, Project


class ProfileForm(forms.ModelsForm):

    class Meta:
        model = Profile
        fields = ('skills', 'projects')

        widgets = {  # The first object in the tuple is the external representation, the second the internal
            'skills': forms.SelectMultiple(choices=[(str(obj), obj) for obj in Skill.objects.all()],
                                           attrs={'class': 'ui multiple search selection dropdown'})
        }
