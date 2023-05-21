from django.urls import path
import account.views as views
urlpatterns = [
    path('',views.index,name="index"),
    path('executivemanagement/',views.coursestatic,name="coursestatic"),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('add-profile-details/', views.add_profile_details, name='add-profile-details'),
    path('logout/', views.handlelogout, name='handlelogout'),
    path('access-pending/', views.access_pending_view, name='access-pending-view'),
]