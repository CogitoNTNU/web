from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from single_page.models import SinglePage


class SinglePageCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'single_page.add_single_page'
    model = SinglePage
    fields = '__all__'


class SinglePageChangeView(PermissionRequiredMixin, UpdateView):
    permission_required = 'single_page.change_single_page'
    model = SinglePage
    fields = '__all__'
    pass


class SinglePageDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'single_page.delete_single_page'
    model = SinglePage
    pass
