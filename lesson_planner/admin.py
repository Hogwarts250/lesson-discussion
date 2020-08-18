from django.contrib import admin

from .models import Lesson, StudentStatus

# Register your models here.
admin.site.register(Lesson)
admin.site.register(StudentStatus)