from django.contrib import admin
from .models import (
    Course,
    Unit,
    Lesson,
    LessonFile,
    LessonLink,
    LessonProgress,
    Announcement,
    AnnouncementFile,
    AnnouncementLink,
    Assignment,
    AssignmentFile,
    AssignmentLink,
    AssignmentSubmission
)

admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Lesson)
admin.site.register(LessonFile)
admin.site.register(LessonLink)
admin.site.register(LessonProgress)
admin.site.register(Announcement)

# Register your models here.
