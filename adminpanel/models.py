from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db.models import Sum
from django.contrib.auth.models import User




def validate_future_date(value):
    if value < now().date():
        raise ValidationError("The date cannot be in the past.")
    
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    

class Organizer(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)  

    def __str__(self):
        return self.user.username
    
class Event(models.Model):
    event_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event_images/',null=True,blank=True)
    description = models.TextField()
    event_date = models.DateField()
    organizer = models.ForeignKey(User,on_delete=models.CASCADE) #user organizing the event
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)#added category
    start_time = models.DateTimeField() #  actual event start time
    end_time = models.DateTimeField() # actual event end time
    capacity = models.IntegerField(null=True,blank=True) # max number of attendees allowed   
    venue = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vip_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def update_available_tickets(self):
        """ Updates available tickets based on confirmed registrations. """
        confirmed_tickets = self.registration_set.filter(is_confirmed=True).aggregate(
            total=models.Sum("ticket_quantity")
        )["total"] or 0
        self.capacity = max(0, self.capacity - confirmed_tickets)
        self.save()
        
    def __str__(self):
        return f"{self.event_name} - {self.event_date}" 
    

class Attendee(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True,null=True,blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    events = models.ManyToManyField("Event", through="Registration")
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.email})"  # Display t
    
class Registration(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee,on_delete=models.CASCADE) 
    registration_date = models.DateTimeField(auto_now_add=True)
    ticket_type = models.CharField(max_length=50,choices=[
        ('Regular','Regular'),
        ('VIP','VIP')
    ])
    ticket_quantity = models.PositiveIntegerField(default=1)
    is_confirmed = models.BooleanField(default=False) #confirmation for registration
    
        
    def __str__(self):
        return f"{self.attendee} registered for {self.event} ({self.ticket_type})({self.ticket_quantity} tickets)"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event','attendee'],name='unique_registration')
        ]
            
class Ticket(models.Model):
    TICKET_TYPES = [
        ('Regular','Regular'),
        ('VIP','VIP')
    ]
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee,on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=10,choices=TICKET_TYPES)
    ticket_quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    ticket_booked = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.attendee.name} - {self.event.event_name} - {self.ticket_type}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event','attendee','ticket_type'], name='unique_ticket')
        ]
        