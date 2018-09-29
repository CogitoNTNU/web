from django import forms
from django.db import OperationalError

from .models import Profile, Skill, Project


class ProfileForm(forms.ModelForm):
    # Because of potential problems with user uploaded images (uploading of explicit content)
    # I've disabled user uploaded profile pictures for the time being. Also cant get it to work on
    # the production server

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        choices = [(str(obj), obj) for obj in Skill.objects.all()]
        self.fields['skills'] = forms.ChoiceField(widget=forms.SelectMultiple(), choices=choices)

    class Meta:
        model = Profile
        # fields = ('picture', 'skills', )
        fields = ('skills', )

        """
        def clean(self):
            picture = self.cleaned_data.get('picture', False)
            if picture:
                if picture.__size > 4 * 1024 * 1024:
                    raise forms.ValidationError("Image file too large ( > 4mb )")
                return picture
            else:
                raise forms.ValidationError("Couldn't read uploaded image")
        """


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('title', 'description', 'form_link', 'application_end')

        widgets = {
            'application_end': forms.DateInput(attrs={'medium': 'date',
                                                      'class': 'ui input left icon',
                                                      'id': 'application_end',
                                                      'type': 'date'}),
            'form_link': forms.URLInput(),
        }
