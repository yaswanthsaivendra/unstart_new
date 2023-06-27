from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (
    Announcement, AnnouncementFile, AnnouncementLink,
    Events, EventsFile, EventsLink,
    Contact
    )
from django.core.mail import send_mail
from account.models import (
    Student_profile_application,
    Teacher_profile_application,
    Student_profile,
    Teacher_profile,
    Profile,
    )
from django.conf import settings
from itertools import chain
from courses.forms import userform
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views import View
from django.urls import reverse_lazy, reverse


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
                profile.status = 't'
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
                profile.status = 's'
                profile.is_verified = True
                profile.save(update_fields = ['is_verified'])


            return redirect(reverse('manager:application-details', kwargs={'pk': pk, 'status': status}))

        elif action == 'reject':
            if status == 't':
                ## reject teacher application
                teacher_application = Teacher_profile_application.objects.filter(id=pk).first()
                teacher_application.is_rejected = True
                teacher_application.save(update_fields=['is_rejected'])

            elif status == 's':
                student_application = Student_profile_application.objects.filter(id=pk).first()
                student_application.is_rejected = True
                student_application.save(update_fields=['is_rejected'])

            return redirect(reverse('manager:application-details', kwargs={'pk': pk, 'status': status}))


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
    template_name = 'manager/announcement_detail.html'
    fields = ['title', 'description']
    context_object_name = 'announcement'

    def get_success_url(self):
        return reverse_lazy('manager:announcement-detail', kwargs={'pk': self.object.pk})



def AnnouncementStatusUpdateView(request, pk):
    announcement = Announcement.objects.filter(id=pk).first()
    if announcement.status == 'released':
        announcement.status = 'draft'
    elif announcement.status == 'draft':
        announcement.status = 'released'
    announcement.save(update_fields = ['status'])
    return redirect('manager:announcement-list')



class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'manager/announcement_detail.html'
    context_object_name = 'announcement'

def announcement_add_link(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.method == 'POST':
        link_url = request.POST.get('link_url')
        AnnouncementLink.objects.create(announcement=announcement, link=link_url)
        return redirect('manager:announcement-detail', pk=pk)

def announcement_delete_link(request, pk, link_pk):
    link = get_object_or_404(AnnouncementLink, pk=link_pk)
    announcement_pk = link.announcement.pk
    link.delete()
    return redirect('manager:announcement-detail', pk=announcement_pk)


def announcement_add_file(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            AnnouncementFile.objects.create(announcement=announcement, file=file)
    return redirect('manager:announcement-detail', pk=pk)

def announcement_delete_file(request, pk, file_pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    file = get_object_or_404(AnnouncementFile, pk=file_pk)
    file.delete()
    return redirect('manager:announcement-detail', pk=pk)

class EventsListView(ListView):
    model = Events
    template_name = 'manager/events.html'
    context_object_name = 'events'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        released_events = self.get_queryset().filter(status='released')
        draft_events= self.get_queryset().filter(status='draft')

        context['released_events'] = released_events
        context['draft_events'] = draft_events

        return context


class EventsCreateView(CreateView):
    model = Events
    template_name = 'manager/events.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('manager:events-list')

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.profile
        return super().form_valid(form)


class EventsUpdateView(UpdateView):
    model = Events
    template_name = 'manager/events_detail.html'
    fields = ['title', 'description']
    context_object_name = 'events'

    def get_success_url(self):
        return reverse_lazy('manager:events-detail', kwargs={'pk': self.object.pk})

def EventsStatusUpdateView(request, pk):
    events = Events.objects.filter(id=pk).first()
    if events.status == 'released':
        events.status = 'draft'
    elif events.status == 'draft':
        events.status = 'released'
    events.save(update_fields = ['status'])
    return redirect('manager:events-list')

class EventsDetailView(DetailView):
    model = Events
    template_name = 'manager/events_detail.html'
    context_object_name = 'events'

def events_add_link(request, pk):
    events = get_object_or_404(Events, pk=pk)

    if request.method == 'POST':
        link_url = request.POST.get('link_url')
        EventsLink.objects.create(events=events, link=link_url)
        return redirect('manager:events-detail', pk=pk)

def events_delete_link(request, pk, link_pk):
    link = get_object_or_404(EventsLink, pk=link_pk)
    events_pk = link.events.pk
    link.delete()
    return redirect('manager:events-detail', pk=events_pk)


def events_add_file(request, pk):
    events = get_object_or_404(events, pk=pk)
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            EventsFile.objects.create(events=events, file=file)
    return redirect('manager:events-detail', pk=pk)

def events_delete_file(request, pk, file_pk):
    events = get_object_or_404(events, pk=pk)
    file = get_object_or_404(EventsFile, pk=file_pk)
    file.delete()
    return redirect('manager:events-detail', pk=pk)


class StudentProfileListView(View):
    def get(self, request):
        students = Student_profile.objects.all()
        return render(request, 'manager/student_profile_list.html', {'students': students})

class TeacherProfileListView(View):
    def get(self, request):
        teachers = Teacher_profile.objects.all()
        return render(request, 'manager/teacher_profile_list.html', {'teachers': teachers})

class ManagerProfileListView(View):
    def get(self, request):
        teachers = Teacher_profile.objects.all()
        return render(request, 'manager/teacher_profile_list.html', {'teachers': teachers})


class StudentProfileDetailView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student_profile, pk=pk)
        return render(request, 'student_profile_detail.html', {'student': student})

class TeacherProfileDetailView(View):
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher_profile, pk=pk)
        return render(request, 'teacher_profile_detail.html', {'teacher': teacher})

class ManagerProfileDetailView(View):
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher_profile, pk=pk)
        return render(request, 'teacher_profile_detail.html', {'teacher': teacher})


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


# def manager_event(request):
#     event = events.objects.filter(user = request.user)
#     allevents=events.objects.all()
#     return render(request,'events.html',{"events":event,"allevents":allevents})


# def update_man_not(request, obj):
#     if obj == 'notification':
#         id = request.POST.get('id')

#         instance = Manager_notification.objects.get(pk = id)
#         form = ManagerNotificationForm(request.POST, instance=instance)
#         if form.is_valid():

#             form.save(commit=False)
#             form.user = request.user
#             form.save()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#     if obj == 'news':
#             id = request.POST.get('id')
#             instance = News_feed.objects.get(pk = id)
#             form = NewsFeedForm(request.POST, instance=instance)
#             if form.is_valid():
#                 form.save(commit=False)
#                 form.user = request.user
#                 form.save()
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#     if obj == 'events':
#             id = request.POST.get('id')
#             instance = Manager_Eveng.objects.get(pk = id)
#             form = ManagerEventForm(request.POST, instance=instance)
#             if form.is_valid():
#                 print('e')
#                 form.save(commit=False)
#                 form.user = request.user
#                 form.save()
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))