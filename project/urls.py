from django.urls import path
from django.views.generic import ListView, DetailView

from project.models import Project
from project.views import administrate_project, accept_applicant, reject_applicant, DeleteProjectView, EditProjectView, \
    apply_to_project, CreateProjectView

urlpatterns = [
    path('', ListView.as_view(model=Project), name='project_list'),
    path('<int:pk>/admin/', administrate_project, name='project_admin'),

    path('<int:pk>/accept/<username>/', accept_applicant, name='accept_applicant'),
    path('<int:pk>/reject/<username>/', reject_applicant, name='reject_applicant'),

    path('<int:pk>/delete/', DeleteProjectView.as_view(), name='delete_project'),
    path('<int:pk>/edit/', EditProjectView.as_view(), name='edit_project'),
    path('<int:pk>/apply/', apply_to_project, name='apply_to_project'),
    path('<int:pk>/', DetailView.as_view(model=Project), name='project'),
    path('new/', CreateProjectView.as_view(), name='project_form'),
]
