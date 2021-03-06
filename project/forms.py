from django import forms

from project.models import Project, Collection


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection'].widget.attrs['class'] = 'ui multiple search selection dropdown'

    class Meta:
        model = Project
        fields = ('title', 'description', 'thumbnail', 'collection',)
