from django.contrib import admin

from .models import Series, Lesson, StudentStatus

# Register your models here.
admin.site.register(Series)
admin.site.register(Lesson)
admin.site.register(StudentStatus)