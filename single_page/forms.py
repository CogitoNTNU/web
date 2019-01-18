from django import forms
from django.urls import resolve, Resolver404

from single_page.models import SingleImage, SinglePage


def conflicting_urls(slug):
    url = f'/{slug}/'
    try:
        res = resolve(url)  # error -> url doesn't exist
        if not res.view_name == 'single_page':  # possible single_page overlap
            return True
    except Resolver404:
        return False


class SingleImageForm(forms.ModelForm):

    class Meta:
        model = SingleImage
        fields = '__all__'


class SinglePageForm(forms.ModelForm):

    class Meta:
        model = SinglePage
        fields = '__all__'

    def clean(self):
        slug = self.cleaned_data.get('slug', None)
        if slug is not None and conflicting_urls(slug):
            raise forms.ValidationError("url already resolves to some other path")
