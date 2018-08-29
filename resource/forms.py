from django import forms
from django.db import OperationalError

from .models import Resource, Tag

class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = ['title', 'creator', 'link', 'description', 'grade', 'medium', 'tags', ]

        # Not sure if the try/except-clause is necessary, but better safe than sorry
        try:
            widgets = {
                'tags': forms.SelectMultiple(choices=[(obj, str(obj)) for obj in Tag.objects.all()],
                                             attrs={'class': 'ui multiple search selection dropdown'}),
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
        except OperationalError:
            pass


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
