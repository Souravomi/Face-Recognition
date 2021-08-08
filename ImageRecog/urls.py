from django.urls import path
from . import views

urlpatterns = [
    path('Camera/',views.openCamera,name='Camera'),
    path('SaveImage/',views.SaveImage,name='SaveImage'),
    path('Predict/',views.RecogninzeImage,name='Predict'),
    path('MarkAttendance/',views.MarkAttendance,name='MarkAttendance'),
    path('Manually/',views.Manually,name='Manually'),
]