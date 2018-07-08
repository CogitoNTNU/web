from django.conf.urls import url

from .views import ProfileDetailView, specific_profile, self_profile

urlpatterns = [
    url(r'(?P<username>[-\w.]+)/$', specific_profile, name='profile'),
    #url(r'info/skills/$')
    #url(r'profile/(?P<username>[-\w.]+)/$', profile, name='profile'),
]