from datetime import timedelta
from django.db.models import Q
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import UpdateView

from concurrency.models import ConcurrentModel


class ConcurrentUpdate(UpdateView):
    timeout = 30

    def get(self, request, *args, **kwargs):
        if request.GET.get('override_edit', 'false') == 'true':
            q = Q()
        else:
            q = Q(concurrency_key=None) | Q(concurrency_time__lte=timezone.now() - timedelta(seconds=60 * self.timeout))

        access = self.model.objects.filter(
            pk=self.kwargs['pk']
        ).filter(q).update(
            concurrency_key=ConcurrentModel.generate_key(),
            concurrency_time=timezone.now(),
            concurrency_user=request.user,
        )
        if not access:
            return render(request, 'concurrency/access_denied.html', {'object': self.get_object()})
        try:
            self.fields = (*self.fields, 'concurrency_key')
        except TypeError:
            self.fields = (*self.form.base_fields, 'concurrency_key')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['concurrency_key'].widget = forms.HiddenInput()
        return context

    def post(self, request, *args, **kwargs):
        try:
            self.fields = (*self.fields, 'concurrency_key')
        except TypeError:
            self.fields = (*self.form.base_fields, 'concurrency_key')
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            own = self.object.concurrency_key == form.data.get('concurrency_key', '')

            if request.GET.get('cancel', 'false') == 'true':
                if own:
                    self.object.concurrency_reset()
                self.updated = False
                return HttpResponseRedirect(self.get_success_url())

            if own or request.GET.get('override_save', 'false') == 'true':
                self.updated = True
                response = super().post(request, *args, **kwargs)
                self.object.concurrency_reset()
                return response
            else:
                form.add_error('concurrency_key', 'Concurrency conflict')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)
