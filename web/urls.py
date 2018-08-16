from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from contentbox.models import ContentBox
from dataporten.views import Logout, login_wrapper
from groups.views import CommitteeList
from web.views import Home

urlpatterns = [
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
    path('resource/', include('resource.urls')),
    path('profiles/', include('user_profile.urls')),
    ContentBox.url('about'),
]
