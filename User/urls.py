from django.urls import path
from . import views

urlpatterns = [
    path('',views.Login,name='Login'),
    path('Home/',views.Home,name='Home'),
    path('Admin_Home/',views.Admin_Home,name='Admin_Home'),
    path('Profile/',views.Profile,name='Profile'),
    path('EditProfile/',views.EditProfile,name='EditProfile'),
    path('Services/',views.Services,name='Services'),
    path('Search/',views.Search,name='Search'),
    path('Security/',views.Security,name='Security'),
    path('Up_Pic/',views.Up_Pic,name='Up_Pic'),
    path('Logout/',views.Logout,name='Logout'),
]