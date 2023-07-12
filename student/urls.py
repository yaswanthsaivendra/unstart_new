from django.urls import path
from .views import (
    index,
    enrolled_courses,
    course_detail_view,
    course_units_view
)


app_name = 'student'


urlpatterns = [
    path('', index, name='home'),
    path('courses/', enrolled_courses, name='enrolled-courses'),
    path('course/<int:course_id>/', course_detail_view, name='course-detail'),
    path('course/<int:course_id>/units/', course_units_view, name='course-units-view'),
]