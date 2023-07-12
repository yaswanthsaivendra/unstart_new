from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.models import User, auth
from django.views.generic import UpdateView, DetailView
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.conf import settings
from .models import Profile, Student_profile_application, Teacher_profile_application,Contact
from django.core.mail import send_mail

def index(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        number=request.POST['number']
        interest=request.POST['interest']
        message = '\n\nfrom\n'+name+'\n'+email
        subject = 'Mail from '+name
        c = Contact.objects.create(name=name, email=email, number=number,interest=interest)
        c.save()
        send_mail(subject, message, settings.EMAIL_HOST_USER, ['saipavansaketh@gmail.com'], fail_silently=False)
    return render(request,'mainindex.html')

def coursestatic(request):
    return render(request,'staticcourse.html')

def aboutus(request):
    return render(request,'mainabout.html')

def teach(request):
    return render(request,'mainteach.html')

def contactus(request):
    return render(request,'maincontact.html')

def privacy(request):
    return render(request,'mainprivacy.html')

def hire(request):
    return render(request,'mainhire.html')

class RegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.error(request, "Please logout to signup")
            return redirect('index')
        else:
            return render(request, 'register.html')

    def post(self, request):
        # create a user account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'username': username,
            'email': email
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password is too short')
                    return render(request, 'register.html')
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = True
                user.save()
                user = auth.authenticate(
                        username=username, password=password)
                if user:
                    auth.login(request, user)
                messages.success(
                    request, 'Account successfully created! Please do login to access Lms')
                return redirect('add-profile-details')

            messages.warning(request, "This Email already exists!")
            return render(request, 'register.html', context)
        else:
            messages.warning(request, "This username already exists!")
            return render(request, 'register.html', context)

class VerificationView(View):
    def get(self, request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            auth.login(request, user,
                    backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        else:
            return render(request, 'registration/login.html')

# def handlelogin(request):
#     if request.method == 'POST':
#         # Get the Post parametres
#         loginusername = request.POST['username']
#         loginpassword = request.POST['password']

#         user = authenticate(username=loginusername, password=loginpassword)
#         user_verify = User.objects.get(username=loginusername)

#         if user.profile.status == 't':
#             login(request, user)
#             messages.success(request, "Successfully logged in")
#             return redirect('teacher_home')
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Successfully logged in")
#             return redirect('home')
#         elif user_verify.is_active == False:
#             messages.error(request, "Please verify your email first to login.")
#             return redirect('home')
#         else:
#             messages.error(request, "Invalid Credentials: Please try again")
#             return redirect('home')
#     return render(request,'login.html')


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            messages.success(request, "Already loggedin")
            return redirect('index')
        else:
            return render(request,'login.html')

    def post(self, request):
        # if 'login_page' in request.POST:
        next = request.POST.get('next')
        username = request.POST['username']
        password = request.POST['password']
        context = {
            'user_found': True,
            'user_name': username
        }
        if username and password:
            if User.objects.filter(username=username).exists():
                user = auth.authenticate(
                    username=username, password=password)
                if user:
                    if user.is_active:
                        auth.login(request, user)
                        messages.success(request, "Successfully logged in")
                        if next:
                            return redirect(next)
                        # return redirect("index")

                        if user.profile.status == 't':
                            if user.profile.is_verified == False:
                                return redirect('access-pending-view')
                            else:
                                return redirect('teacher:home')
                        elif user.profile.status == 's':
                            if user.profile.is_verified == False:
                                return redirect('access-pending-view')
                            else:
                                return redirect('student:home')
                        elif user.profile.status == 'm':
                            return redirect('manager:home')
                        else:
                            return redirect('home')

                    messages.error(
                        request, "Account is not active,please check your email"
                    )

            elif User.objects.filter(email=username).exists():
                user = User.objects.get(email=username)
                user = auth.authenticate(
                    username=user.username, password=password)

                if user:
                    if user.is_active:
                        auth.login(request, user)
                        messages.success(request, "Successfully logged in")
                        if next:
                            return redirect(next)
                        # return redirect("index")
                        if user.profile.status == 't':
                            if user.profile.is_verified == False:
                                return redirect('access-pending-view')
                            else:
                                return redirect('teacher:home')
                        elif user.profile.status == 's':
                            if user.profile.is_verified == False:
                                return redirect('access-pending-view')
                            else:
                                return redirect('student:home')
                        elif user.profile.status == 'm':
                            return redirect('manager:home')
                        else:
                            return redirect('home')

                    messages.error(
                        request, "Account is not active,please check your email"
                    )
            elif (User.objects.filter(email=username).exists() or User.objects.filter(username=username).exists() == False):
                messages.error(
                    request, "The username or Email you have entered does not exist.")
                return render(request, 'login.html', context)

        context = {
            'user_found': True,
            'user_name': username
        }
        messages.error(request, 'Invalid credentials, try again')
        return render(request, 'login.html', context)

        # return render(request, "login.html")

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('index')

def add_profile_details(request):
    if request.method == 'GET':
        return render(request, 'account/add_profile_details.html')

    elif request.method == 'POST':
        ## getting user profile
        user_profile = Profile.objects.filter(user=request.user).first()

        ## get the status - teacher or student
        status = request.POST.get('status')
        # print(request.POST)
        # print(request.FILES)


        if status == 's':
            semester = request.POST.getlist('semester')[0]
            section = request.POST.getlist('section')[0]
            roll_number = request.POST.getlist('roll_number')[0]
            full_name = request.POST.getlist('full_name')[0]
            department = request.POST.getlist('department')[0]
            profile_pic = request.FILES.getlist('profile_pic')[0]
            Student_profile_application.objects.create(
                profile=user_profile,
                semester=semester,
                section=section,
                roll_number=roll_number,
                full_name=full_name,
                department =department
            )

        elif status == 't':
            date_of_joining = request.POST.get('date_of_joining')
            semester = request.POST.getlist('semester')[1]
            section = request.POST.getlist('section')[1]
            full_name = request.POST.getlist('full_name')[1]
            department = request.POST.getlist('department')[1]
            profile_pic = request.FILES.getlist('profile_pic')[0]
            Teacher_profile_application.objects.create(
                profile=user_profile,
                date_of_joining=date_of_joining,
                semester=semester,
                section=section,
                full_name=full_name,
                department=department
            )
        user_profile.profile_pic = profile_pic
        user_profile.status = status
        user_profile.save(update_fields=['profile_pic', 'status'])
        return redirect('access-pending-view')


def edit_profile_details(request, application_id):
    # Retrieve the user profile
    user_profile = Profile.objects.filter(user=request.user).first()

    if request.method == 'GET':
        # Pass the user profile to the template
        if user_profile.status == 's':
            print("student")
            student_profile = Student_profile_application.objects.filter(id = application_id).first()
            return render(request, 'account/edit_student_application_profile_details.html', {'user_profile': user_profile, 'student_profile' : student_profile})
        if user_profile.status == 't':
            teacher_profile = Teacher_profile_application.objects.filter(id = application_id).first()
            return render(request, 'account/edit_teacher_application_profile_details.html', {'user_profile': user_profile, 'teacher_profile' : teacher_profile})


    elif request.method == 'POST':
        ## getting user profile
        user_profile = Profile.objects.filter(user=request.user).first()
        # print(request.POST)
        # print(request.FILES)

        if user_profile.status == 's':
            student_profile = Student_profile_application.objects.filter(id=application_id).first()
            student_profile.semester = request.POST.get('semester')
            student_profile.section = request.POST.get('section')
            student_profile.roll_number = request.POST.get('roll_number')
            student_profile.full_name = request.POST.get('full_name')
            student_profile.department = request.POST.get('department')
            profile_pic = request.FILES.get('profile_pic')
            student_profile.save()

        elif user_profile.status == 't':
            teacher_profile = Teacher_profile_application.objects.filter(id=application_id).first()
            teacher_profile.date_of_joining = request.POST.get('date_of_joining')
            teacher_profile.semester = request.POST.get('semester')
            teacher_profile.section = request.POST.get('section')
            teacher_profile.full_name = request.POST.get('full_name')
            teacher_profile.department = request.POST.get('department')
            profile_pic = request.FILES.get('profile_pic')
            teacher_profile.save()
        user_profile.profile_pic = profile_pic
        user_profile.save(update_fields=['profile_pic'])
        return redirect('access-pending-view')




def access_pending_view(request):
    if request.method == 'GET':
        user_profile = Profile.objects.filter(user=request.user).first()
        student_applications = Student_profile_application.objects.filter(profile__in= [user_profile])
        teacher_applications = Teacher_profile_application.objects.filter(profile__in= [user_profile])

        show_new_application_button = not (
        teacher_applications.filter(is_rejected=False).exists() or
        student_applications.filter(is_rejected=False).exists()
        )

        return render(request, 'account/access_pending.html', {
            'student_applications': student_applications,
            'teacher_applications' : teacher_applications,
            'show_new_application_button': show_new_application_button
        })



def events(request):
    return render(request,'student/events_page.html')



