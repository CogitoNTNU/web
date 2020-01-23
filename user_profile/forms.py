from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args)
        self.fields['skills'].form = forms.SelectMultiple()
        self.fields['skills'].widget.attrs['class'] = 'ui multiple search selection dropdown'
        # set 'skills' initial value to the skills already registered to the user
        skill_set = kwargs.get('skills', [])
        skills = [skill['id'] for skill in skill_set]
        self.fields['skills'].initial = skills

    class Meta:
        model = Profile
        fields = ('picture', 'skills', )

        def clean(self):
            picture = self.cleaned_data.get('picture', False)
            if picture:
                if picture.__size > 4 * 1024 * 1024:
                    raise forms.ValidationError("Image file too large ( > 4mb )")
                return picture
