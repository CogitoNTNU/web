from django.conf.urls import url

from .views import profile, DetailSkillView

urlpatterns = [
    url(r'(?P<username>[-\w.]+)/$', profile, name='profile'),
    url(r'skill/(?P<pk>\d+)$', DetailSkillView.as_view(), name='skill_detail'),
    ]

