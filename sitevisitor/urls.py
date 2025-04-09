from django.urls import path
from .import views


app_name = 'sitevisitor'

urlpatterns = [
    
    path('',views.home,name='home'),
    path('event_list/',views.event_list,name='event_list'),
    path('event_details/<int:event_id>/',views.event_details,name='event_details'),
    path('event_booking/<int:id>/',views.event_booking,name='event_booking'),
    path('login/',views.loginn,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/',views.profile_view,name='profile'),
    path('reset_password/',views.reset_password,name="reset_password")
    ]
    


