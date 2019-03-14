from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.views.generic import RedirectView

from contentbox.models import ContentBox
from dataporten.views import Logout, login_wrapper
from groups.views import CommitteeList
from web import settings
from web.views import Home

urlpatterns = [

    path('robots.txt/', lambda x: HttpResponse(robots_text, content_type='text/plain'), name='robots_text'),

    path('admin/', admin.site.urls),
    path('complete/<str:backend>/', login_wrapper),
    path('', include('social_django.urls', namespace='social')),
    path('', Home.as_view(), name='home'),
    path('login/', RedirectView.as_view(url='/login/dataporten/'), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('news/', include('news.urls')),
    path('contentbox/', include('contentbox.urls')),
    path('committees/', CommitteeList.as_view(), name='committees'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('resources/', include('resource.urls')),
    path('profiles/', include('user_profile.urls')),
    path('projects/', include('project.urls')),
    ContentBox.url('about'),
    ContentBox.url('about/statutes'),
    ContentBox.url('about/business'),
    path('', include('single_page.urls'), name='single_page'),

]

handler404 = 'web.views.handler404'

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

with open('robots.txt', 'r') as r:
    robots_text = r.read()
