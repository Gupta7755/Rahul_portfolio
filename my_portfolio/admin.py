from django.contrib import admin
from .models import *
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(About)
admin.site.register(Experience)
admin.site.register(Certificate)
admin.site.register(Education)
admin.site.register(Resume)
admin.site.register(Skill)
admin.site.register(Feedback)
admin.site.site_header = "Rahul's Portfolio Admin"
