from django.contrib import admin

from .models import (
    temp_verification,
    Student_profile_application,
    Teacher_profile_application,
    Student_profile,
    Teacher_profile,
    Profile,
    Notification,
    Contact
    )

admin.site.register(temp_verification)
admin.site.register(Student_profile_application)
admin.site.register(Teacher_profile_application)
admin.site.register(Student_profile)
admin.site.register(Contact)
admin.site.register(Profile)
admin.site.register(Teacher_profile)
admin.site.register(Notification)