from django.urls import path
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .models import Skill
from .views import SkillListView, SkillDetailView

from .views import profile

urlpatterns = [

    path('skills/', SkillListView.as_view(), name='skill_list'),

    path('skill/<int:pk>/', SkillDetailView.as_view(), name='skill'),

    # must always be at the end, else it will interpret skill, project etc. as usernames
    path('<str:username>/', profile, name='profile'),
    ]
