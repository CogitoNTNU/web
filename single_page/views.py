from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView

from single_page.forms import SinglePageForm, SingleImageForm
from single_page.models import SinglePage, SingleFile, SingleImage


class SingleImageDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'single_page.delete_singleimage'
    model = SingleImage
    template_name = 'web/confirm_delete.html'
    success_url = '/'


class SingleImageCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'single_page.add_singleimage'
    template_name = 'single_page/singlepage_form.html'
    model = SingleImage
    form_class = SingleImageForm


class SinglePageCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'single_page.add_singlepage'
    form_class = SinglePageForm
    template_name = 'single_page/singlepage_form.html'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['files'] = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
        return form

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if form.is_valid():
            self.object = form.save()
            for file in files:
                SingleFile.objects.create(file=file, page=self.object)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class SinglePageUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'single_page.change_singlepage'
    model = SinglePage
    form_class = SinglePageForm
    template_name = 'single_page/singlepage_form.html'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['files'] = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
        form.fields['delete_files'] = forms.BooleanField(
            widget=forms.CheckboxInput, required=False, label='Delete previously uploaded files'
        )
        return form

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        self.object = self.get_object()
        if form.is_valid():
            if form.cleaned_data.pop('delete_files', False):
                slug = kwargs['slug']
                for file in SingleFile.objects.filter(page__slug=slug):
                    file.delete()
            for file in files:
                SingleFile.objects.create(file=file, page=self.object)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SinglePageDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'single_page.delete_singlepage'
    model = SinglePage
    template_name = 'web/confirm_delete.html'
    success_url = '/'


def image_view(request, slug):
    image = SingleImage.objects.get(slug=slug)
    image_data = open(image.image.path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")

