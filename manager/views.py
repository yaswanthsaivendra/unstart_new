from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import *
# Create your views here.

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