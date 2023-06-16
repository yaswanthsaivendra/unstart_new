from django.urls import path
from .views import (
    enrolled_courses
)


app_name = 'student'


urlpatterns = [
    path('courses/', enrolled_courses, name='enrolled-courses'),
]