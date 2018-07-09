from django.conf.urls import url

from .views import profile

urlpatterns = [
    url(r'(?P<username>[-\w.]+)/$', profile, name='profile'),
    #url(r'info/skills/$')
    ]