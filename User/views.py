from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from User.models import Student,Academic,Attandance

# Create your views here.


def Login(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']

        try: 
            user = auth.authenticate(username=username,password=password)
           
        except:
            user = None

        if user is not None and user.is_staff == 1:
            
            auth.login(request,user)
            request.session['username'] = username
            
            return redirect("Admin_Home")

        elif user is not None and user.is_staff == 0:
            
            auth.login(request,user)
            request.session['username'] = username

            return redirect("Home")

        else:
           messages.success(request,'Incorrect Username or Password!')
           return render(request,'User/Login.html')
    else:
        return render(request,'User/Login.html')



@login_required(login_url='/Login')
def Home(request):
    return render(request,'User/Home.html')


@login_required(login_url='/Login')
def Admin_Home(request):
    if 'ap' in request.POST:
        val = request.POST['ID']
        
        Att = Attandance.objects.get(id=val)
        Att.Active = 'Present'
        Att.save()
        messages.success(request,'Current Password Is Incorrect!')
        return redirect('Admin_Home')
    elif 'rej' in request.POST:
        val = request.POST['ID']
        
        Att = Attandance.objects.get(id=val)
        Att.Active = 'Absent'
        Att.save()
        messages.success(request,'Current Password Is Incorrect!')
        return redirect('Admin_Home')
    else:    
        data = Attandance.objects.filter(Active='Pending')
        return render(request,'Admin/Home.html',{'data':data})


@login_required(login_url='/Login')
def Profile(request):
    user = User.objects.get(username=request.session['username'])
    view = Student.objects.get(Email=user)
    return render(request,'User/Profile.html',{'val':view})


@login_required(login_url='/Login')
def EditProfile(request):
    if request.method == "POST":
        addr1 = request.POST['addr1']
        addr2 = request.POST['addr2']
        addr3 = request.POST['addr3']
        Pin = request.POST['pin']
        Mob = request.POST['mob']

        user = User.objects.get(username=request.session['username'])
        val = Student.objects.get(Email = user)
        val.Addr_1 = addr1
        val.Addr_2 = addr2
        val.Addr_3 = addr3
        val.Pincode = Pin
        val.Mobile = Mob
        val.save()
        return redirect('Profile')
    else:
        user = User.objects.get(username=request.session['username'])
        val = Student.objects.get(Email = user)
        return render(request,'User/Edit_Profile.html',{'val':val})


@login_required(login_url='/Login')
def Services(request):
    user = User.objects.get(username=request.session['username'])
    val = Student.objects.get(Email = user)
    return render(request,'User/Services.html',{'val':val})


@login_required(login_url='/Login')
def Search(request):
    if request.method == "POST":
        val = request.POST['month']
        #print(val)
        user = User.objects.get(username=request.session['username'])
        stud = Student.objects.get(Email=user)
        #Att = Attandance.objects.filter(Date__month__gte=val,Stud_Id=stud)
        #print(Att)
        Att = Attandance.objects.filter(Stud_Id=stud,Date__month=val)
        #print(new)
        return render(request,'User/Search_Attandance.html',{'data':Att})
    else:    
        user = User.objects.get(username=request.session['username'])
        stud = Student.objects.get(Email=user)
        Att = Attandance.objects.filter(Stud_Id=stud)
        return render(request,'User/Search_Attandance.html',{'data':Att})


@login_required(login_url='/Login')
def Up_Pic(request) :

    if request.method == 'POST' :
        user = User.objects.get(username=request.session['username'])
    
        demo = Student.objects.get(Email = user)
        demo.image = request.FILES.get('file')

        demo.save()

        return redirect('Services')

    else:
        return render(request,'User/Services.html')



@login_required(login_url='/Login')
def Security(request):

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
            return redirect('Services')

    else:
        return redirect('Services')



def Logout(request):
    request.session.flush()
    auth.logout(request)
    return redirect('/')