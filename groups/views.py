from django.views.generic import ListView

from groups.models import Committee


class CommitteeList(ListView):
    model = Committee
    template_name = 'groups/committee_list.html'
