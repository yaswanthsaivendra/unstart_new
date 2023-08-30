from django.contrib import admin
from .models import (
    Course,
    Unit,
    Lesson,
    LessonFile,
    LessonLink,
    LessonProgress,
    Announcement,
    Timetable,
    Syllabus,
    AnnouncementFile,
    AnnouncementLink,
    Assignment,
    AssignmentFile,
    AssignmentLink,
    AssignmentSubmission,
    Enrollment,
)



class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__',)

admin.site.register(Course, CourseAdmin)

# admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Lesson)
admin.site.register(LessonFile)
admin.site.register(LessonLink)
admin.site.register(LessonProgress)
admin.site.register(Announcement)
admin.site.register(Enrollment)
admin.site.register(Timetable)
admin.site.register(Syllabus)

# Register your models here.
