from django.urls import path
from .views import (
    index,
    enrolled_courses,
    course_detail_view,
    course_units_view,
    allcourses,
    calender,
    communication,
    course_detail,
    course_learning,
    course_tools,
    notifications_page,
    course_content,
    assignments,
    assignments_detail,
    course_tasks,
    unit_launch
)


app_name = 'student'


urlpatterns = [
    path('', index, name='home'),
    path('courses/', enrolled_courses, name='enrolled-courses'),
    path('course/<int:course_id>/', course_detail_view, name='course-detail'),
    path('course/<int:course_id>/units/', course_units_view, name='course-units-view'),
    path('courses/allcourses',allcourses,name="allcourses"),
    path('courses/calender',calender,name="calender"),
    path('courses/communication',communication,name="communication"),
    path('courses/course_learning',course_learning,name="course_learning"),
    path('courses/course_tools',course_tools,name="course_tools"),
    path('courses/notifications_page',notifications_page,name="notifications"),
    path('courses/course_content',course_content,name="course_content"),
    path('courses/assignments',assignments,name="assignments"),
    path('courses/assignments_detail',assignments_detail,name="assignments_detail"),
    path('courses/course_tasks',course_tasks,name="course_tasks"),
    path('courses/unit_launch',unit_launch,name="unit_launch"),
]