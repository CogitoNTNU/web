from django import forms
from django.db import OperationalError

from .models import Resource, Tag


class ResourceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.fields['tags'].form = forms.SelectMultiple()
        self.fields['tags'].widget.attrs['class'] = 'ui multiple search selection dropdown'

    class Meta:
        model = Resource
        fields = ['title', 'content_creator', 'link', 'description', 'grade', 'medium', 'tags', ]

        widgets = {
            'medium': forms.Select(choices=(
                                    ("Course", "Course"),
                                    ("Paper", "Paper"),
                                    ("Book", "Book"),
                                    ("Online-course", "Online course"),
                                    ("Video", "Video"),
                                    ("Other", "Other"),
                            )),
            'grade': forms.Select(choices=(
                                ("beginner", "Beginner"),
                                ("intermediate", "Intermediate"),
                                ("advanced", "Advanced"),
                            )),
            'link': forms.URLInput(),
        }


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name', )

    def clean(self):
        name = str(self.cleaned_data['name']).upper()
        other_tags = [str(t).upper() for t in Tag.objects.all()]
        if not all(c.isalnum() or c.isspace() for c in name):
            raise forms.ValidationError("Tags can only contain alphanumerical characters")
        if name in other_tags:
            raise forms.ValidationError("This tag already exists")
