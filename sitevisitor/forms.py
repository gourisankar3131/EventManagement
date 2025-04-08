from django import forms 
from adminpanel.models import Attendee,Ticket,Registration,Event




class AttendeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name','email','phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
class EventRegistrationForm(forms.ModelForm):
     class Meta:
         model = Registration
         fields = ['event','attendee','ticket_type']
         widgets = {
             'event': forms.Select(attrs={'class':'form-select'}),
             'attendee': forms.Select(attrs={'class':'form-select'}),
             'ticket_type':forms.Select(attrs={'class':'form-control'}),
         }

class TicketBookingForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event','attendee','ticket_type','ticket_quantity']