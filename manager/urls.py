from django.urls import path
from . import views


urlpatterns = [
    path('manager-home/', views.manager_home, name='manager-home'),
    path('application-details/<str:status>/<int:pk>/', views.application_details, name='application-details'),

    path('contact/', views.contact, name='contact'),
    path('events/', views.manager_event, name='events'),
]