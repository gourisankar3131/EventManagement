from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from adminpanel import models
from django.core.mail import send_mail
from django.conf import settings
from sitevisitor.models import UserProfile
from adminpanel.models import Event,Attendee,Registration
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request,'sitevisitor/home.html')


def profile_view(request):
    profile,created = UserProfile.objects.get_or_create(user=request.user)
    return render(request,'sitevisitor/profile.html',{'profile':profile})

def reset_password(request):
    return render(request,'reset_password.html')

def loginn(request):
    if request.method == "POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            if user.is_staff:
                login(request,user)
                messages.success(request,"Login successfully")
                return redirect('adminpanel:dashboard')
            else:
                login(request,user)
                messages.success(request,'Login successfully') 
                return redirect('sitevisitor:home')
        else:
            messages.error(request,'Invalid username or password.Try again!')
        return redirect('sitevisitor:login')
    
    return render(request, 'sitevisitor/login.html') 

def register(request):
        if request.method == "POST":
            username = request.POST.get('username')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken. Please choose another one!!!')
                return redirect('sitevisitor:register') 
        
            if password1 != password2:
                messages.error(request,"Password doesn't match , Try again!!!")
                return redirect('sitevisitor:register')
            else:
                my_user=User.objects.create_user(username=username,
                                                first_name=firstname,
                                                last_name=lastname,
                                                email=email,
                                                password=password1)
                my_user.save() 
            messages.success(request,"User created successfully")
            return redirect('sitevisitor:login')   
            
        return render(request,'sitevisitor/signup.html')

@login_required(login_url='/login/')
def event_list(request):
      events = Event.objects.all()
      return render(request,'sitevisitor/event_list.html',{'events':events})

@login_required(login_url='/login/')
def event_details(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    is_sold_out = event.capacity <= 0 
    return render(request,'sitevisitor/event_detail.html',{'event':event,"is_sold_out": is_sold_out})

@login_required(login_url='/login/')
def event_booking(request,id):
    event = get_object_or_404(Event, id=id)

    # Prevent superusers from booking
    if request.user.is_superuser:
        messages.error(request, "Super admins are not allowed to book events.")
        return redirect("sitevisitor:event_list")

    #  attendee exists or not
    attendee, created = Attendee.objects.get_or_create(user=request.user)

    # Check the event is fully booked
    if event.capacity <= 0:
        messages.error(request, "Sorry, this event is fully booked!")
        return redirect("sitevisitor:event_list")

    if request.method == "POST":
        if not event.requires_ticket:
            # Register attendee for free events
            registration, created = Registration.objects.get_or_create(
                event=event,
                attendee=attendee,
                defaults={"ticket_quantity": 1, "ticket_type": "RSVP", "is_confirmed": True}
            )
            messages.success(request, "You are now registered for the event.")
        
        else:
            # Handle ticketed events
            ticket_quantity = int(request.POST.get("ticket_quantity", 1))
            ticket_type = request.POST.get("ticket_type", "Regular")

            if ticket_quantity > event.capacity:
                messages.error(request, "Not enough tickets available!")
                return redirect("sitevisitor:event_booking", id=event.id)

            #Create or update registration
            registration, created = Registration.objects.get_or_create(
                event=event,
                attendee=attendee,
                defaults={"ticket_quantity": ticket_quantity, "ticket_type": ticket_type, "is_confirmed": True}
            )

            if not created:
                registration.ticket_quantity += ticket_quantity
                registration.save()

            #  Updating event capacity
            event.capacity -= ticket_quantity
            event.save()

            messages.success(request, "Booking successful! A confirmation email has been sent.")

            #  Send confirmation email
            subject = f"Event Booking Confirmation: {event.event_name}"
            message = (
                f"Dear {attendee.user.first_name},\n\n"
                f"You have successfully booked {ticket_quantity} ticket(s) for '{event.event_name}'.\n"
                f"Event Date: {event.event_date}\n\n"
                f"Thank you for booking. We look forward to seeing you at the event!\n\n"
                f"Best regards,\n"
                f"Event Management Team"
            )
            recipient_list = [attendee.user.email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        return redirect("sitevisitor:event_list")

    return render(request, "sitevisitor/event_booking.html", {"event": event})
    
    
@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    messages.success(request,'You were logged out!!!')
    return redirect('sitevisitor:home')