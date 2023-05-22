from django.contrib import admin
from .models import Contact,mainpagenews,testimonials,mainwebsite,news,events,Announcement

# Register your models here.

admin.site.register(Contact)
admin.site.register(mainpagenews)
admin.site.register(testimonials)
admin.site.register(mainwebsite)
admin.site.register(events)
admin.site.register(Announcement)
admin.site.register(news)
