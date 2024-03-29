from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from teacher.models import (
    Enrollment,
    Course,
    LessonProgress,
)
from django.utils import timezone

@login_required
def enrolled_courses(request):
    enrolled_courses = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'student/enrolled_courses.html', {'enrolled_courses': enrolled_courses})


@login_required
def course_detail_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    student = request.user
    enrollment = Enrollment.objects.filter(student=student, course=course).first()
    # Update the last_accessed field to the current timestamp
    enrollment.last_accessed = timezone.now()
    enrollment.save()
    units = course.unit_set.all()

    unit_progress = []
    for unit in units:
        lessons_total = unit.lesson_set.count()
        lessons_completed = LessonProgress.objects.filter(enrollment=enrollment, lesson__unit=unit, is_completed=True).count()
        completion_percentage = (lessons_completed / lessons_total) * 100 if lessons_total > 0 else 0
        unit_progress.append((unit, completion_percentage, lessons_completed, lessons_total))

    context = {
        'course': course,
        'enrollment': enrollment,
        'unit_progress': unit_progress,
    }

    return render(request, 'student/course_detail.html', context)



def course_units_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    units = course.unit_set.all()

    for unit in units:
        unit.lessons = unit.lesson_set.all()

    context = {
        'course': course,
        'units': units,
    }

    return render(request, 'student/course_learning_page.html', context)


def index(request):
    total_course_enrollments = Enrollment.objects.filter(student=request.user).select_related('course').order_by('-last_accessed')
    recently_accessed_course_enrollments = total_course_enrollments[:6]
    total_course_enrollments_count = total_course_enrollments.count()

    context = {
        'recently_accessed_course_enrollments' : recently_accessed_course_enrollments,
        'total_course_enrollments_count' : total_course_enrollments_count
    }
    return render(request, 'student/index.html', context)


def allcourses(request):
    return render(request,'student/enrolled_courses.html')

def calender(request):
    return render(request,'student/calender_page.html')

def communication(request):
    return render(request,'student/communication_page.html')

def course_detail(request):
    return render(request,'student/course_detail.html')

def course_learning(request):
    return render(request,'student/course_learning_page.html')

def course_tools(request):
    return render(request,'student/course_tools_page.html')

def notifications_page(request):
    return render(request,'student/notifications_page.html')

def course_content(request):
    return render(request,'student/course_learning_page.html')

def assignments(request):
    return render(request,'student/assignments.html')

def assignments_detail(request):
    return render(request,'student/assignments_detail.html')

def course_tasks(request):
    return render(request,'student/course_tasks.html')

def unit_launch(request):
    return render(request,'student/unit_launch.html')