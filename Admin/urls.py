from django.urls import path
from . import views

urlpatterns = [
    path('',views.Main,name='Main'),
    path('New_Admission',views.New_Admission,name='New_Admission'),
    path('Search_Studant',views.Search_Studant,name='Search_Studant'),
    path('Edit_Studant',views.Edit_Studant,name='Edit_Studant'),
    path('View_Attandance',views.View_Attandance,name='View_Attandance'),
    path('Settings',views.Settings,name='Settings'),
    path(r'^export/csv/$',views.Excel,name='Excel'),
]