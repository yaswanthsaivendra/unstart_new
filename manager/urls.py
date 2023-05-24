from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('home/', views.manager_home, name='home'),
    path('application-details/<str:status>/<int:pk>/', views.application_details, name='application-details'),

    path('announcements/', views.AnnouncementListView.as_view(), name='announcement-list'),
    path('announcements/create/', views.AnnouncementCreateView.as_view(), name='announcement-create'),
    path('announcements/<int:pk>/update/', views.AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('announcements/<int:pk>/statusupdate/', views.AnnouncementStatusUpdateView, name='announcement-status-update'),
    path('announcements/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('announcements/<int:pk>/add-link/', views.announcement_add_link, name='announcement-add-link'),
    path('announcements/<int:pk>/delete_link/<int:link_pk>/', views.announcement_delete_link, name='announcement-delete-link'),
    path('announcements/<int:pk>/add-file/', views.announcement_add_file, name='announcement-add-file'),
    path('announcements/<int:pk>/delete_file/<int:file_pk>/', views.announcement_delete_file, name='announcement-delete-file'),


    path('students/', views.StudentProfileListView.as_view(), name='student-profile-list'),
    path('teachers/', views.TeacherProfileListView.as_view(), name='teacher-profile-list'),



    # path('contact/', views.contact, name='contact'),
    # path('events/', views.manager_event, name='events'),
]