from django import forms

from project.models import Project


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applicant_pool'].form = forms.SelectMultiple()
        self.fields['applicant_pool'].widget.attrs['class'] = 'ui multiple search selection dropdown'

    class Meta:
        model = Project
        fields = ('title', 'description', 'applicant_pool', 'application_end',)

        widgets = {
            'application_end': forms.DateInput(attrs={'medium': 'date',
                                                      'class': 'ui input left icon',
                                                      'id': 'application_end',
                                                      'type': 'date'}),
            'form_link': forms.URLInput(),
        }