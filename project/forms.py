from django import forms

from project.models import Project, Collection


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection'].widget.attrs['class'] = 'ui multiple search selection dropdown'
        self.fileds['collection'].label = 'Collection'  # Should be translated to norwegian

    class Meta:
        model = Project
        fields = ('title', 'description', 'thumbnail', 'collection',)
        labels = ('Tittel', 'Beskrivelse', 'Thumbnail', 'Collection')  # Collection should be translated to norwegian
