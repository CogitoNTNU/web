from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        skill_set = kwargs.get('skills', [])  # Gets value skills from kwargs if exists, if not default is an empty list
        skills = [skill['id'] for skill in skill_set]
        super(ProfileForm, self).__init__(*args)
        self.fields['skills'].form = forms.SelectMultiple()
        self.fields['skills'].widget.attrs['class'] = 'ui multiple search selection dropdown'
        self.fields['skills'].initial = skills  # Sets initial value to skills SelectMany field
        self.fields['picture'].widget.attrs['enctype'] = 'multipart/form-data'

    class Meta:
        model = Profile
        fields = ('picture', 'skills', )

        def clean(self):
            picture = self.cleaned_data.get('picture', False)
            if picture:
                if picture.__size > 4 * 1024 * 1024:
                    raise forms.ValidationError("Image file too large ( > 4mb )")
                return picture
