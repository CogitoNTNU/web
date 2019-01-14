from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from single_page.models import SinglePage, SingleFile, ImagePage


class SinglePageCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'single_page.add_singlepage'
    model = SinglePage
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['files'] = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
        return form

    def form_valid(self, form):
        try:
            for file in form.cleaned_data.pop('files'):
                SingleFile.objects.create(file=file, feed=self.object)
        except TypeError:
            pass
        return super().form_valid(form)


class SinglePageChangeView(PermissionRequiredMixin, UpdateView):
    permission_required = 'single_page.change_singlepage'
    model = SinglePage
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['files'] = forms.FileField(widget=forms.FileInput(
            attrs={'multiple': '', 'enctype': 'multipart/form-data'}), required=False
        )
        return form

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if form.is_valid():
            for file in files:
                SingleFile.objects.create(file=file, feed=self.object)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SinglePageDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'single_page.delete_singlepage'
    model = SinglePage
    template_name = 'web/confirm_delete.html'


def image_view(request, slug):
    image = ImagePage.objects.get(slug=slug)
    image_data = open(image.image.path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")
