from django import forms
from django.core.exceptions import ValidationError
from django.db import OperationalError

from .models import Profile, Skill, Project


class ProfileForm(forms.ModelForm):
    # Because of potential problems with user uploaded images (uploading of explicit content)
    # I've disabled user uploaded profile pictures for the time being. Also cant get it to work on
    # the production server

    class Meta:
        model = Profile
        # fields = ('picture', 'skills', )
        fields = 'skills'

        try:
            widgets = {  # The first object in the tuple is the external representation, the second the internal
                'skills': forms.SelectMultiple(choices=[(str(obj), obj) for obj in Skill.objects.all()],
                                               attrs={'class': 'ui multiple search selection dropdown'}),
            }
        except OperationalError:
            pass

        """
        def clean(self):
            picture = self.cleaned_data.get('picture', False)
            if picture:
                if picture.__size > 4 * 1024 * 1024:
                    raise ValidationError("Image file too large ( > 4mb )")
                return picture
            else:
                raise ValidationError("Couldn't read uploaded image")
        """


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('title', 'description', 'form_link', 'application_end')

        widgets = {
            'application_end': forms.DateInput(attrs={'medium': 'date',
                                                      'class': 'ui input left icon',
                                                      'id': 'application_end'}),
            'form_link': forms.URLInput(),
        }
