from django.contrib import admin
from django.contrib.admin import ModelAdmin
from myapp.models import *

admin.site.register(CV)
admin.site.register(CustomUser)
admin.site.register(WorkField)
admin.site.register(Job)

