from django import forms
from .models import Profile, Skill, Project


class ProfileForm(forms.ModelsForm):

    class Meta:
        model = Profile
        fields = ('skills', 'projects')

        widgets = {
            'skills': forms.SelectMultiple(choices=[(str(obj), str(obj)) for obj in Skill.objects.all()],
                                           attrs={'class': 'ui multiple search selection dropdown'})
        }
