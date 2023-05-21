from django.urls import path
from . import views

urlpatterns = [
    path('contact', views.contact, name='contact'),
    path('events', views.manager_event, name='events'),
]