from django.contrib import admin
from django.urls import path

from web.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
]
