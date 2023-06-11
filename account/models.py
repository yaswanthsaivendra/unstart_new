from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import datetime
from django.utils import timezone
# from django.core.validators import MaxValueValidator
# Create your models here.
from django.utils.text import slugify
import hashlib

def get_unique_string(body, time):
    s = str(body)+str(time)
    result_str = hashlib.sha1(s.encode()).hexdigest()[:10]
    return result_str


class College(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# #User._meta.get_field('email')._unique = True

# def current_year():
#         return datetime.date.today().year

# def max_value_current_year(value):
#     return MaxValueValidator(current_year()+10)(value)


gender_choices = (('M', 'MALE'),
('F', 'FEMALE'),
('O', 'OTHER'))

class Profile(models.Model):

    status_choices = [
    ('p', 'Principal'),
    ('t', 'Teacher'),
    ('s', 'Student'),
    ('m','Management')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # personal details
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    email                   =       models.EmailField()
    college = models.ForeignKey(College,on_delete = models.CASCADE,null=True, blank=True)
    slug = models.SlugField(max_length=200, editable=False, null=True, blank=True)
    status = models.CharField(choices=status_choices, max_length=5, default='s')
    is_verified = models.BooleanField(default=False)



    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(Profile, self).save()
        self.slug = slugify(self.user.username)
        super(Profile, self).save()

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    number = models.CharField(max_length=200)
    interest=models.CharField(max_length=200)
    def __str__(self):
        return 'Msg from '+self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Student_profile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    semester                =       models.CharField(max_length=10)
    section                =       models.CharField(max_length=10)
    roll_number         = models.IntegerField(blank=True,null=True)
    full_name               =       models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=500, null=True, blank=True)


class Teacher_profile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    date_of_joining = models.DateField()
    semester                =       models.CharField(max_length=10)
    section                =       models.CharField(max_length=10)
    full_name               =       models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=500, null=True, blank=True)



class Student_profile_application(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    semester                =       models.CharField(max_length=10)
    section                =       models.CharField(max_length=10)
    roll_number         = models.IntegerField(blank=True,null=True)
    full_name               =       models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=500, null=True, blank=True)
    requested_on = models.DateField(default =timezone.now)
    request_seen = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)



class Teacher_profile_application(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_of_joining = models.DateField()
    semester                =       models.CharField(max_length=10)
    section                =       models.CharField(max_length=10)
    full_name               =       models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=500, null=True, blank=True)
    requested_on = models.DateField(default=timezone.now)
    request_seen = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)






class temp_verification(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    college = models.ForeignKey(College,on_delete=models.DO_NOTHING)
    semester                =       models.CharField(max_length=10)
    section                =       models.CharField(max_length=10)
    Year                =       models.DateField(default=datetime.datetime.now)
    roll_number         = models.IntegerField(blank=True,null=True)
    department = models.CharField(max_length=500, null=True, blank=True)
    is_varified         = models.BooleanField(default=False)
    is_rejected         = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_notifications')
    image = models.ImageField(upload_to='notifications')
    body = models.TextField()
    url = models.URLField(null=True, blank=True)
    url_name = models.CharField(max_length=255, default='View', null=True, blank=True)
    notified_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=16, null=True, unique=True, editable=False)

    def __str__(self):
        return self.profile.user.username + ' ' + self.body[0:15]

    def save(self, *args, **kwargs):
        super(Notification, self).save()
        self.slug = slugify(get_unique_string(self.body, self.notified_time))
        super(Notification, self).save()

