from django.contrib import admin
from django.urls import path, include

from web.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('news/', include('news.urls')),
]
