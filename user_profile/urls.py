from django.conf.urls import url

from .views import profile, DetailSkillView, DetailProjectView, CreateProjectView, apply_to_project

urlpatterns = [
    url(r'skill/(?P<pk>\d+)$', DetailSkillView.as_view(), name='skill'),
    url(r'project/(?P<pk>\d+)/apply/$', apply_to_project, name='apply_to_project'),
    url(r'project/(?P<pk>\d+)$', DetailProjectView.as_view(), name='project'),
    url(r'project/new/$', CreateProjectView.as_view(), name='project_form'),

    # must always be at the end, else it will interpret skill, project etc. as usernames
    url(r'(?P<username>[-\w.]+)/$', profile, name='profile'),
    ]

