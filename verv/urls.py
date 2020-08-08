from django.urls import path
from django.views.generic import ListView, DetailView

from verv.models import Verv, VervGroup
from verv.views import DeleteVervView, \
    EditVervView, CreateVervView, CreateVervGroupView

urlpatterns = [
    path('', ListView.as_view(queryset=VervGroup.objects.filter(verv__isnull=False).distinct(), paginate_by=3), name='vervgroup_list'),
    path('vervgroup/<int:pk>/', DetailView.as_view(model=VervGroup), name='vervgroup'),
    path('vervgroup/new/', CreateVervGroupView.as_view(), name='vervgroup_form'),
    path('verv/<int:pk>/delete/', DeleteVervView.as_view(), name='delete_verv'),
    path('verv/<int:pk>/edit/', EditVervView.as_view(), name='edit_verv'),
    path('verv/<int:pk>/', DetailView.as_view(model=Verv), name='verv'),
    path('verv/new/', CreateVervView.as_view(), name='verv_form'),
]
