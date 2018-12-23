from django import forms

from project.models import Project, Collection


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collection'].widget.attrs['class'] = 'ui multiple search selection dropdown'

    collection = forms.ModelChoiceField(required=False, queryset=Collection.objects.all())
    application_end = forms.DateField()
    application_end.widget_attrs = {'type': 'date'}

    class Meta:
        model = Project
        fields = ('title', 'description', 'collection',)

        widgets = {
            'application_end': forms.DateInput(attrs={'medium': 'date',
                                                      'class': 'ui input left icon',
                                                      'id': 'application_end',
                                                      'type': 'date'}),
            'form_link': forms.URLInput(),
        }