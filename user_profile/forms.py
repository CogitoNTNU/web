from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    # Because of potential problems with user uploaded images (uploading of explicit content)
    # I've disabled user uploaded profile pictures for the time being. Also cant get it to work on
    # the production server

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['skills'].form = forms.SelectMultiple()
        self.fields['skills'].widget.attrs['class'] = 'ui multiple search selection dropdown'

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

