from django.urls import path
from . import views


urlpatterns = [
    path('manager-home/', views.manager_home, name='manager-home'),
    path('application-details/<str:status>/<int:pk>/', views.application_details, name='application-details'),

    path('announcements/', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('announcements/create/', views.AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcements/<int:pk>/update/', views.AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('announcements/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement_detail'),

    path('contact/', views.contact, name='contact'),
    path('events/', views.manager_event, name='events'),
]