from django.shortcuts import render
from django.http import HttpResponse
<<<<<<< HEAD
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from .auth_utils import std_authenticate, std_login, std_logout, get_student
from .models import AdminSetting, Student, Section, Course, CourseVolunteer, Form, CustomUser
=======
>>>>>>> parent of fbc6a56 (完成學員登入系統)

# Create your views here.

def index(request):
<<<<<<< HEAD
    return render(request, 'index.html')

def stdLogin(request):
    if request.method == 'POST':
        std_id = request.POST['std_id']
        team = request.POST['team']
        satb = request.POST['satb']
        print(std_id, team, satb)
        student = std_authenticate(std_id=std_id, team=team, satb=satb)

        if student is not None:
            std_login(request, student)
            print('login success')
            return redirect('/pSel')
        else:
            messages.info(request, '無法登入，請檢查資料是否正確')
            print('login failed')
            return redirect('/stdLogin')
    else:
        return render(request, 'stdLogin.html')

def vLogin(request):
    if request.method == 'POST':
        password = request.POST['password']

        user = auth.authenticate(password=password)

        if password is not None:
            auth.login(request, user)
            return redirect('/dashboard')
        else:
            return redirect('/vLogin')
    else:
        return render(request, 'vLogin.html')

def pSel(request):
    if request.session.has_key('std_id'):

        std_id = request.session['std_id']
        team = request.session['team']
        JorH = request.session['JorH']
        student = {'std_id': std_id, 'team': team, 'JorH': JorH}
        return render(request, 'pSel.html', {'student': student})
    else:
        return redirect('/stdLogin')
=======
    return render(request, 'index.html')
>>>>>>> parent of fbc6a56 (完成學員登入系統)
