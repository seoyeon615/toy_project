from django.contrib import admin
from .models import Department, Course, Professor, ExamReview

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Professor)
admin.site.register(ExamReview)