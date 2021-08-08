from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import os
import os.path
import sys
import base64
import uuid
import cv2
import codecs
from PIL import Image
from io import BytesIO
from pathlib import Path
from cvmodule.Face_Recog import test,train
from cvmodule import create_csv
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from User.models import Student,Attandance,Academic
from django.contrib import messages




def openCamera(request):
    id = request.session['Studentid']
    return render(request, 'ImageRecog/Camera.html',{'id':id})

# save incoming images to corresponding folders

@csrf_exempt
def SaveImage(request):
    if request.method == 'POST':
        uid = request.POST['id']
        img = request.POST['TrainFace']
        indx = img.find(",") + 1
        img= img[indx:] 
        path='cvmodule/Training_Data/'
        if not os.path.exists(path+uid):
            os.mkdir(path+uid)
        imgdata = base64.b64decode(img)
        filename = path+uid+'/'+str(uuid.uuid4())+'.png' 
        with open(filename, 'wb') as f:
            f.write(imgdata)
        
    return HttpResponse("Image saved")

# call this route when to predict a face . send the facedata along with request


def MarkAttendance(request):
    # exec(open("cvmodule/create_csv.py").read())
    return render(request,"ImageRecog/Recognize.html")

@csrf_exempt
def RecogninzeImage(request):
    if request.method == 'POST':
        facedata = request.POST['FaceData']
        indx = facedata.find(",") + 1
        facedata= facedata[indx:] 
        path='ImageRecog/Temp/'
        imgdata = base64.b64decode(facedata)
        name = str(uuid.uuid4())
        filename = path+name+'.png' 
        print(filename)
        with open(filename, 'wb') as f:
            f.write(imgdata)
        result = test(filename, train())
        print("--------------------------------------------------------------------")
        print('Accuracy')
        print(result[1])
        

        if add(result[0],result[1]):
            user = User.objects.get(username=request.session['username'])
            stud = Student.objects.get(Email = user)
            academic = Academic.objects.get(Stud_Id=stud)
            Att = Attandance(Stud_Id=stud,Active='Present',Reason="Face Found",Course=academic.Course)
            Att.save()
            print("Saved")
        else:
            print("Not Added")

        return JsonResponse({
        "id":result[0],
        "confidence":result[1]
        })
        
    else:
        return render(request,'ImageRecog/Recognize.html')
        #return redirect('Home')

def add(id,conf):
    if conf < 60:
        print("==========================================================================")
        print('True')
        print("==========================================================================")
        return True
    else:
        print("==========================================================================")
        print('FAlse')
        print("==========================================================================")
        return False


def Manually(request):
    if request.method == "POST":
        Reason = request.POST['reson']

        user = User.objects.get(username=request.session['username'])
        stud = Student.objects.get(Email = user)
        academic = Academic.objects.get(Stud_Id=stud)
        Att = Attandance(Stud_Id=stud,Active='Pending',Reason=Reason,Course=academic.Course)
        #print(Att)
        Att.save()
        return redirect('Home')
    else:
        return render(request,'ImageRecog/Recognize.html')
    


