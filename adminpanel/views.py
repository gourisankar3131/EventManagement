from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Category,Event,Attendee
from .forms import CategoryForm,EventForm,AttendeeForm
from django.http import HttpResponseForbidden
 #Create your views here.

def admin(request):
        return render(request,'adminpanel/dashboard.html')

def admin_profile(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")
    return render(request, 'adminpanel/profile.html', {'user': request.user})

def dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access the admin panel.")
        return redirect('adminpanel:login')  # Redirect for non-superusers
    
    # Count total events, categories, and attendees
    total_events = Event.objects.count()
    total_categories = Category.objects.count()
    total_attendees = Attendee.objects.count()

    context = {
        'total_events': total_events,
        'total_categories': total_categories,
        'total_attendees': total_attendees
    }
    return render(request,'adminpanel/dashboard.html',context)
    
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            if user.is_staff:
                login(request,user)
                messages.success(request,"Admin login successfull")
                return redirect('adminpanel:dashboard')
            else:
                messages.error(request, "You are not authorized to access the admin panel.")
                return redirect('sitevisitor:login')
        
        else:
            messages.error(request, "Invalid username or password. Try again!")
            return redirect('adminpanel:login')
        
    return render(request,'adminpanel/login.html')

def logout_view(request):
    logout(request)
    messages.success(request,'You were logged out!!!')
    return render(request,'adminpanel/logout.html')

def create_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'A new category added successfully!!!')
            return redirect('adminpanel:category_list')
    
        else:
            form = CategoryForm
    return render(request,'adminpanel/add_category.html',{'form':form})

def category_list(request):
    categories = Category.objects.all()
    return render(request,'adminpanel/category_list.html',{'categories':categories})

def add_attendee(request):
    users = User.objects.all()
    form = AttendeeForm()
    if request.method == "POST":
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save(commit=False)
            attendee.user = request.user
            attendee.save()
            messages.success(request,'You have successfully registere as an attendee') 
            return redirect('adminpanel:dashboard')
        else:
            form = AttendeeForm()
           
    return render(request,'adminpanel/add_attendee.html',{'form':form,'users':users})

def attendee_list(request):
    attendee = Attendee.objects.all()
    return render(request,'adminpanel/attendee_list.html',{'attendee':attendee})

def create_event(request):
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"New event is added successfully!")
            return redirect('adminpanel:event_list')
        else:
            form = EventForm()
    return render(request,'adminpanel/create_event.html',{'form':form})

@login_required(login_url='/login/')
def event_list(request):
      events = Event.objects.all()
      return render(request,'adminpanel/event_list.html',{'events':events})

@login_required(login_url='/login/')
def event_detail(request):
    events = Event.objects.all()
    return render(request,'adminpanel/event_detail.html',{'events':events})

@login_required(login_url='/login/')
def delete_event(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    if request.method =='POST':
        event.delete()
        messages.success(request,"Event delete successfully")
        return redirect('adminpanel:event_detail')
    
    return render(request,'adminpanel/delete_event.html',{'event':event})




    


