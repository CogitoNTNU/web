from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from contentbox.models import ContentBox
from dataporten.views import Logout, login_wrapper
from web.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('', Home.as_view(), name='home'),
    path('login/', RedirectView.as_view(url='/login/dataporten/'), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    re_path(r'^complete/(?P<backend>[^/]+){0}/$', login_wrapper),
    path('news/', include('news.urls')),
    path('contentbox/', include('contentbox.urls')),
    ContentBox.url('about'),
]
