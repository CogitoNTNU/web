from django.contrib import admin
from .models import Skill, Project, Profile

admin.site.register(Skill)
admin.site.register(Profile)
admin.site.register(Project)