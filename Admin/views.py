from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from User.models import Student,Academic,Attandance
from datetime import datetime
from datetime import date
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import csv

# Create your views here.


@login_required(login_url='/Login')
def Main(request):
    return render(request,'Admin/Base_Admin.html')


@login_required(login_url='/Login')
def New_Admission(request):
    if request.method == 'POST':
        request.session['Studentid'] = ""
        Name = request.POST['name']
        Gender = request.POST['gender']
        DOB = request.POST['dob']
        Country = request.POST['contry']
        Addr_1 = request.POST['Addr1']
        Addr_2 = request.POST['Addr2']
        Addr_3 = request.POST['Addr3']
        Pincode = request.POST['pin']
        Mobile = request.POST['mob']
        Email = request.POST['email']
        Qualification = request.POST['qual']
        Percentage = request.POST['per']
        Course = request.POST['course']
        Program = request.POST['prog']
        Qual_Doc = request.FILES['myid']
        Std_Image = request.FILES['myimg']

        #Auto Id Generation
   
        myDate = datetime.now() 
        Y = myDate.strftime("%Y")  
        if Course == 'BCA':
            C = '10'
        elif Course == 'Bcom':
            C = '20'
        elif Course == 'BBA':
            C = '30'
        elif Course == 'Mcom':
            C = '40'
        if Course == 'MCA':
            C = '50'
        elif Course == 'MBA':
            C = '60'

        X =  Y + C

        try:
            count = Student.objects.filter(Stud_Id__contains=X).count()
        except:
            count = 0

        if count == 0:
            n = "100"
            X = X + str(n)
        else:
            n = count + 1
            X = X + str(n)

      
        user=User.objects.create_user(username=Email,password=X,email=Email)
        user.save()

        stud = Student(Stud_Id=X,Email = user,Name=Name,DOB=DOB,Gender=Gender,Country=Country,
        Addr_1=Addr_1,Addr_2=Addr_2,Addr_3=Addr_3,Pincode=Pincode,Mobile = Mobile)
        stud.save() 

        Acad = Academic(Stud_Id = stud,Qualification = Qualification,Percentage = Percentage,Course = Course,
        Program = Program,Qual_Doc = Qual_Doc,Std_Image = Std_Image)
        Acad.save()
        request.session['Studentid'] = X
        messages.success(request,'Student Added Successfully! Add Training Images')
        return redirect('New_Admission')
    else:
        return render(request,'Admin/New_Admission.html')


@login_required(login_url='/Login')
def Search_Studant(request):
    if request.method == "POST":
        val = request.POST['Id_num']
        try:
            data = Academic.objects.get(Stud_Id=val)
        except:
            data = None

        if data is not None:
            data = Academic.objects.filter(Stud_Id=val)
            return render(request,'Admin/Search_Studant.html',{'data':data})
        else:
            messages.success(request,'Current Password Is Incorrect!')
            data = Academic.objects.all()
            return render(request,'Admin/Search_Studant.html',{'data':data})

    else:
        data = Academic.objects.all()
        return render(request,'Admin/Search_Studant.html',{'data':data})


@login_required(login_url='/Login')
def Edit_Studant(request):
    if request.method == 'GET':
        Id = request.GET['fieldkey']
        request.session['id'] = Id
        view = Student.objects.get(Stud_Id=Id)
        return render(request,'Admin/Edit_Studant.html',{'view':view})
    elif request.method == 'POST':
        Name = request.POST['name']
        Gender = request.POST['gen']
        Addr1 = request.POST['addr1']
        Addr2 = request.POST['addr2']
        Addr3 = request.POST['addr3']
        Pin = request.POST['pin']
        Mobile = request.POST['mob']

        #user = User.objects.get(username=request.session['username'])
        val = Student.objects.get(Stud_Id = request.session['id'])
        val.Name = Name
        val.Gender = Gender
        val.Addr_1 = Addr1
        val.Addr_2 = Addr2
        val.Addr_3 = Addr3
        val.Pincode = Pin
        val.Mobile = Mobile
        val.save()
        messages.success(request,'Updated')
        view = Student.objects.get(Stud_Id=request.session['id'])
        return render(request,'Admin/Edit_Studant.html',{'view':view})
    else:
        view = Student.objects.get(Stud_Id=request.session['id'])
        return render(request,'Admin/Edit_Studant.html',{'view':view})



@login_required(login_url='/Login')
def View_Attandance(request):
    if  request.method == "POST":
        val = request.POST['Id_num']
        print(val)
        try:
            ac = Student.objects.get(Stud_Id=val)
            data = Attandance.objects.filter(Stud_Id=ac)
        except:
            data = None

        if data is not None:
            ac = Student.objects.get(Stud_Id=val)
            data = Attandance.objects.filter(Stud_Id=ac)
            return render(request,'Admin/Attandance_View.html',{'data':data})
        else:
            messages.success(request,'Current Password Is Incorrect!')
            data = Attandance.objects.all()
            return render(request,'Admin/Attandance_View.html',{'data':data})
    else:
        data = Attandance.objects.all()
        return render(request,'Admin/Attandance_View.html',{'data':data})


@login_required(login_url='/Login')
def Excel(request):
    if request.method == "POST":
        print(date.today())
        course = request.POST['course']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Attandance_' + course + '_' +\
        str(date.today()) + '.csv'

        writer = csv.writer(response)
        writer.writerow(['Studant ID', 'Name',  'Date' , 'Status'])

        #users = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
        corse = Academic.objects.filter(Course=course)

        data = Attandance.objects.filter(Date__date=date.today()).values_list('Stud_Id','Stud_Id__Name','Date','Active')
        for user in data:
            writer.writerow(user)

        return response


@login_required(login_url='/Login')
def Settings(request):
    if request.method == 'POST':

        username = request.session['username']
        current = request.POST['old']
        New = request.POST['psw']
      
        try:
            user = auth.authenticate(username=username,password=current)
           
        except:
            
            user = None
        
        if user is not None :
            user.set_password(New)
            user.save()
            return redirect('Logout')
        else:
            messages.success(request,'Current Password Is Incorrect!')
            return render(request,'Admin/Password_Change.html')

    else:
        return render(request,'Admin/Password_Change.html')