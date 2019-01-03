from django.urls import path
from django.views.generic import ListView, DetailView

from project.models import Project, Collection
from project.views import ProjectAdminDetailView, accept_applicant, reject_applicant, DeleteProjectView, \
    EditProjectView, CreateProjectView, CreateCollectionView, apply_to_collection

urlpatterns = [
    path('', ListView.as_view(model=Collection), name='collection_list'),
    path('collection/<int:pk>/', DetailView.as_view(model=Collection), name='collection'),
    path('collection/new/', CreateCollectionView.as_view(), name='collection_form'),

    path('<int:pk>/admin/', ProjectAdminDetailView.as_view(), name='project_admin'),
    path('<int:pk>/accept/<username>/', accept_applicant, name='accept_applicant'),
    path('<int:pk>/reject/<username>/', reject_applicant, name='reject_applicant'),

    path('project/<int:pk>/delete/', DeleteProjectView.as_view(), name='delete_project'),
    path('project/<int:pk>/edit/', EditProjectView.as_view(), name='edit_project'),
    path('project/<int:pk>/apply/', apply_to_collection, name='apply_to_collection'),
    path('project/<int:pk>/', DetailView.as_view(model=Project), name='project'),
    path('project/new/', CreateProjectView.as_view(), name='project_form'),
]
