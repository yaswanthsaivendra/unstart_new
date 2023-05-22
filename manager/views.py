from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from account.models import (
    Student_profile_application,
    Teacher_profile_application,
    Student_profile,
    Teacher_profile,

    )
from itertools import chain
from courses.forms import userform


@login_required
def manager_home(request):
    if request.method == 'GET':
        # Get all student and teacher applications
        student_applications = Student_profile_application.objects.all()
        teacher_applications = Teacher_profile_application.objects.all()
    
        # Combine and reverse-sort the applications based on 'requested_on'
        all_applications = sorted(
            chain(student_applications, teacher_applications),
            key=lambda x: x.requested_on,
            reverse=True
        )

        # Filter applications based on status
        verified_applications = [app for app in all_applications if app.is_verified]
        rejected_applications = [app for app in all_applications if app.is_rejected]
        pending_applications = [app for app in all_applications if not app.is_verified and not app.is_rejected]
        
        # user form to create new user.
        user_form = userform()
        

        return render(request, 'manager/requests.html', {
        'verified_applications': verified_applications,
        'rejected_applications': rejected_applications,
        'pending_applications': pending_applications,
        "user_form":user_form
        })


@login_required
def application_details(request, pk, status):
    if request.method == 'GET':
        if status == 't':
            application = Teacher_profile_application.objects.filter(id=pk).first()
        elif status == 's':
            application = Student_profile_application.objects.filter(id=pk).first()
        

        return render(request, 'manager/application_details.html', {'application': application })
    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'accept':
            if status == 't':
                ## accept teacher application
                teacher_application = Teacher_profile_application.objects.filter(id=pk).first()
                teacher_application.is_verified = True
                teacher_application.save(update_fields=['is_verified'])
                # create Teacher Profile
                Teacher_profile.objects.create(
                    profile = teacher_application.profile,
                    semester = teacher_application.semester,
                    section = teacher_application.section,
                    full_name = teacher_application.full_name,
                    department = teacher_application.department,
                    date_of_joining = teacher_application.date_of_joining
                )
                # mark the profile as verified
                profile = Profile.objects.filter(id = teacher_application.profile.id).first()
                profile.is_verified = True
                profile.save(update_fields = ['is_verified'])


            elif status == 's':
                student_application = Student_profile_application.objects.filter(id=pk).first()
                student_application.is_verified = True
                student_application.save(update_fields=['is_verified'])

                Student_profile.objects.create(
                    profile = student_application.profile,
                    semester = student_application.semester,
                    section = student_application.section,
                    full_name = student_application.full_name,
                    department = student_application.department,
                    roll_number = student_application.roll_number
                )
                # mark the profile as verified
                profile = Profile.objects.filter(id = student_application.profile.id).first()
                profile.is_verified = True
                profile.save(update_fields = ['is_verified'])
    
           
            return redirect('application-details')

        elif action == 'reject':
            if status == 't':
                ## reject teacher application
                teacher_application = Teacher_profile_application.objects.filter(id=pk).first()
                teacher_application.is_rejected = True
                teacher_application.save(update_fields=['is_rejected'])


            elif status == 's':
                student_application = Student_profile_application.objects.filter(id=pk).first()
                student_application.is_verified = True
                student_application.save(update_fields=['is_verified'])
            
            return redirect('application-details')







@login_required
def contact(request):
	if request.method=='POST':
		message = request.POST['message']
		name = request.POST['name']
		email = request.POST['email']
		message += '\n\nfrom\n'+name+'\n'+email
		subject = 'Mail from '+name
		c = Contact.objects.create(name=name, email=email, msg=message)
		c.save()
		send_mail(subject, message, settings.EMAIL_HOST_USER, ['saipavansaketh@gmail.com'], fail_silently=False)
	return render(request, 'contact.html')


def manager_event(request):
    event = events.objects.filter(user = request.user)
    allevents=events.objects.all()
    return render(request,'events.html',{"events":event,"allevents":allevents})


def update_man_not(request, obj):
    if obj == 'notification':
        id = request.POST.get('id')

        instance = Manager_notification.objects.get(pk = id)
        form = ManagerNotificationForm(request.POST, instance=instance)
        if form.is_valid():

            form.save(commit=False)
            form.user = request.user
            form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if obj == 'news':
            id = request.POST.get('id')
            instance = News_feed.objects.get(pk = id)
            form = NewsFeedForm(request.POST, instance=instance)
            if form.is_valid():
                form.save(commit=False)
                form.user = request.user
                form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if obj == 'events':
            id = request.POST.get('id')
            instance = Manager_Eveng.objects.get(pk = id)
            form = ManagerEventForm(request.POST, instance=instance)
            if form.is_valid():
                print('e')
                form.save(commit=False)
                form.user = request.user
                form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))