from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse

from concurrency.views import ConcurrentUpdate
from contentbox.models import ContentBox


class EditContentBoxView(PermissionRequiredMixin, ConcurrentUpdate):
    model = ContentBox
    template_name = 'contentbox/edit.html'
    fields = (
        'content',
    )
    permission_required = (
        'contentbox.change_contentbox',
    )

    def get_success_url(self):
        return reverse(self.object.title)
