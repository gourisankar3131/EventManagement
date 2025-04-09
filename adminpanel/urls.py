from django.urls import path
from .import views


app_name = 'adminpanel'

urlpatterns = [
    path('admin_base',views.admin,name='admin_base'),
     path('profile/',views.admin_profile, name='admin_profile'),
    path('',views.dashboard,name='dashboard'),
    path('add_category/',views.create_category,name='add_category'),
    path('category_list/',views.category_list,name='category_list'),
    path('add_attendee/',views.add_attendee,name='add_attendee'),
    path('attendee_list/',views.attendee_list,name='attendee_list'),
    path('add_event/',views.create_event,name='add_event'),
    path('event_list/',views.event_list,name='event_list'),
    path('event_detail/',views.event_detail,name='event_details'),
    path('update_event/<int:event_id>/',views.update_event,name="update_event"),
    path('delete_event/<int:event_id>/',views.delete_event,name='delete_event'),
    path('login/',views.admin_login,name='login'),
    path('logout/',views.logout_view,name='logout'),
    
]