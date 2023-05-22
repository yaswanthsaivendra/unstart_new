from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('home/', views.manager_home, name='home'),
    path('application-details/<str:status>/<int:pk>/', views.application_details, name='application-details'),

    path('announcements/', views.AnnouncementListView.as_view(), name='announcement-list'),
    path('announcements/create/', views.AnnouncementCreateView.as_view(), name='announcement-create'),
    path('announcements/<int:pk>/update/', views.AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('announcements/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),

    path('contact/', views.contact, name='contact'),
    path('events/', views.manager_event, name='events'),
]