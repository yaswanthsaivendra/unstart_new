from django.db import models
from account.models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
import hashlib
# Create your models here.

def get_unique_string(body, time):
    s = str(body)+str(time)
    result_str = hashlib.sha1(s.encode()).hexdigest()[:10]
    return result_str

class Announcement(models.Model):

    DRAFT = 'draft'
    RELEASED = 'released'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (RELEASED, 'Released'),
    ]

    user_profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True,null=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)

    slug = models.SlugField(max_length=16, null=True, unique=True, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Announcement, self).save()
        self.slug = slugify(get_unique_string(self.title,self.user_profile))
        super(Announcement, self).save()


class AnnouncementFile(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    file = models.FileField(upload_to='announcement_files/')


class AnnouncementLink(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    link = models.URLField()




class events(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=50,blank=True,null=True)
    description = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField()

    slug = models.SlugField(max_length=16, null=True, unique=True, editable=False)

    def __str__(self):
        return self.title[0:15]

    def save(self, *args, **kwargs):
        super(events, self).save()
        self.slug = slugify(get_unique_string(self.description,self.user))
        super(events, self).save()

class news(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=50,blank=True,null=True)
    description = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField()

    slug = models.SlugField(max_length=16, null=True, unique=True, editable=False)

    def __str__(self):
        return self.announcement[0:15]

    def save(self, *args, **kwargs):
        super(news, self).save()
        self.slug = slugify(get_unique_string(self.description,self.user))
        super(news, self).save()

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

    slug = models.SlugField(max_length=16, null=True, unique=True, editable=False)

    def __str__(self):
        return self.content[0:15]

    def save(self, *args, **kwargs):
        super(testimonials, self).save()
        self.slug = slugify(get_unique_string(self.content,self.user))
        super(testimonials, self).save()

class mainpagenews(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.CharField(max_length=200,blank=True,null=True)
    content = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField()

    slug = models.SlugField(max_length=16, null=True, unique=True, editable=False)

    def __str__(self):
        return self.content[0:15]

    def save(self, *args, **kwargs):
        super(mainpagenews, self).save()
        self.slug = slugify(get_unique_string(self.content,self.user))
        super(mainpagenews, self).save()

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    msg = models.TextField()
    def __str__(self):
        return 'Msg from '+self.name
