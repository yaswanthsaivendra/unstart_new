from django.contrib import admin

# Register your models here.
from .models import temp_verification, Student_profile_application, Teacher_profile_application

admin.site.register(temp_verification)
admin.site.register(Student_profile_application)
admin.site.register(Teacher_profile_application)