from django.urls import path
import account.views as views
urlpatterns = [
    path('',views.index,name="index"),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('events/',views.events,name="events"),
    path('teachwithus/',views.teach,name="teach"),
    path('contactus/',views.contactus,name="contactus"),
    path('privacy/',views.privacy,name="privacy"),
    path('hirefromus/',views.hire,name="hire"),
    path('executivemanagement/',views.coursestatic,name="coursestatic"),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('add-profile-details/', views.add_profile_details, name='add-profile-details'),
    path('edit-profile-details/<int:application_id>/', views.edit_profile_details, name='edit-profile-details'),
    path('logout/', views.handlelogout, name='logout'),
    path('access-pending/', views.access_pending_view, name='access-pending-view'),
]