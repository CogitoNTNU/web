from django import forms

from project.models import Project


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