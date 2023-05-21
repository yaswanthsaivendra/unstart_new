from django.urls import path
import account.views as views
urlpatterns = [
    path('',views.index,name="index"),
    path('executivemanagement/',views.coursestatic,name="coursestatic"),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),
    path('register', views.RegistrationView.as_view(), name='register'),
    path('login', views.handlelogin, name='login'),
]