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
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy


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
        application.request_seen = True
        application.save(update_fields=['request_seen'])
        

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
                profile.status = student_application.status
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




class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'manager/announcements.html'
    context_object_name = 'announcements'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        released_announcements = self.get_queryset().filter(status='released')
        draft_announcements = self.get_queryset().filter(status='draft')
        
        context['released_announcements'] = released_announcements
        context['draft_announcements'] = draft_announcements
        
        return context


class AnnouncementCreateView(CreateView):
    model = Announcement
    template_name = 'manager/announcements.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('manager:announcement-list')

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.profile
        return super().form_valid(form)


class AnnouncementUpdateView(UpdateView):
    model = Announcement
    template_name = 'announcement/announcement_update.html'
    fields = ['announcement', 'status']
    context_object_name = 'announcement'

    def get_success_url(self):
        return reverse_lazy('announcement_detail', kwargs={'pk': self.object.pk})



class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'manager/announcement_detail.html'
    context_object_name = 'announcement'






















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