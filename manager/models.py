from django.db import models
from account.models import *
import datetime
from django.contrib.auth.models import User

# Create your models here.

class announcement(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    announcement = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.user.username

class events(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    announcement = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.user.username

class news(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    announcement = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.user.username

class mainwebsite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    header = models.CharField(max_length=200,blank=True,null=True)
    footer = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.user.username

class testimonials(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.CharField(max_length=200,blank=True,null=True)
    content = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.user.username

class mainpagenews(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.CharField(max_length=200,blank=True,null=True)
    content = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.user.username

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    msg = models.TextField()
    def __str__(self):
        return 'Msg from '+self.name
