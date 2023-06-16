from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from teacher.models import (
    Enrollment,
    Course,
)

@login_required
def enrolled_courses(request):
    enrolled_courses = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'student/enrolled_courses.html', {'enrolled_courses': enrolled_courses})
