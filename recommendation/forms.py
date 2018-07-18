from django import forms
from django.db import OperationalError

from .models import Entry, Tag


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['title', 'creator', 'link', 'description', 'grade', 'type', 'tags', ]

        # Not sure if the try/except-clause is necessary, but better safe than sorry
        try:
            widgets = {
                'tags': forms.SelectMultiple(choices=[(str(obj), str(obj)) for obj in Tag.objects.all()],
                                             attrs={'class': 'ui multiple search selection dropdown'}),
                'type': forms.Select(choices=(
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
        if name in other_tags:
            raise forms.ValidationError("This tag already exists")
