from django import forms

from verv.models import Verv, VervGroup


class VervForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['VervGroup'].widget.attrs['class'] = 'ui multiple search selection dropdown'

    class Meta:
        model = Verv
        fields = ('title', 'description', 'thumbnail', 'VervGroup',)