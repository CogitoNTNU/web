from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import ListView, DetailView
from .models import Project, Skill

from .views import profile, CreateProjectView, apply_to_project, DeleteProjectView, \
    EditProjectView, administrate_project, accept_applicant, reject_applicant

urlpatterns = [
    path('projects/', ListView.as_view(model=Project), name='project_list'),
    path('project/<int:pk>/admin/', administrate_project, name='project_admin'),

    path('project/(<int:pk>/accept/<username>/', accept_applicant, name='accept_applicant'),
    path('project/<int:pk>/reject/<username>/', reject_applicant, name='reject_applicant'),

    path('project/<int:pk>/delete/', DeleteProjectView.as_view(), name='delete_project'),
    path('project/<int:pk>/edit/', EditProjectView.as_view(), name='edit_project'),
    path('project/<int:pk>/apply/', apply_to_project, name='apply_to_project'),
    path('project/<int:pk>/', DetailView.as_view(model=Project), name='project'),
    path('project/new/', CreateProjectView.as_view(), name='project_form'),
    path('skill/<int:pk>/', DetailView.as_view(model=Skill), name='skill'),

    # must always be at the end, else it will interpret skill, project etc. as usernames
    path('<username>/', profile, name='profile'),
    ]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


