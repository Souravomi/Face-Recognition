from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    Stud_Id=models.TextField(primary_key=True)
    Email = models.ForeignKey(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=70,null=True)
    DOB = models.DateField(null=True)
    Gender = models.CharField(max_length=10)
    Country = models.CharField(max_length=20,null=True)
    Addr_1 = models.CharField(max_length=70,null=True)
    Addr_2 = models.CharField(max_length=70,null=True)
    Addr_3 = models.CharField(max_length=70,null=True)
    Pincode = models.CharField(max_length=10,null=True)
    Mobile = models.CharField(max_length=15,null=True)
    image = models.ImageField(default='default.png',upload_to='Profile Pics',null=True)

class Academic(models.Model):
    Stud_Id = models.ForeignKey(Student,on_delete=models.CASCADE)
    Qualification = models.CharField(max_length=70)
    Percentage = models.CharField(max_length=10)
    Course = models.CharField(max_length=10)
    Program = models.CharField(max_length=10)
    Created = models.DateField(auto_now=True)
    Qual_Doc=models.FileField(upload_to='Qualification Document')
    Std_Image=models.ImageField(upload_to='Candidates/')


class Attandance(models.Model):
    Stud_Id = models.ForeignKey(Student,on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now=True)
    Course = models.CharField(max_length=10,null=True)
    Active = models.CharField(max_length=10)
    Reason = models.TextField(null=True)
