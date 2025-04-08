from django.contrib import admin
from .models import Profile,Organizer,Category,Event,Attendee,Registration,Ticket

#Register your models here.

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number') 

admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Attendee)
admin.site.register(Registration)
admin.site.register(Ticket)
admin.site.register(Organizer)
admin.site.register(Profile)