from django import forms
from django.contrib.auth.models import User
from .models import Category,Event,Attendee




    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name','description','organizer','image','category','image','event_date','start_time','end_time','venue','capacity']
    
class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name','email','phone_number']