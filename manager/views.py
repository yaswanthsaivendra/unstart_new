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
    return render(request,'events.html',{"event_form":event_form,"events":event})
