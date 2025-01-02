from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .auth_utils import std_authenticate, std_login, std_logout, get_student
import zipfile, csv, shutil
from django.core.files.storage import FileSystemStorage
from django.db import connection
from .models import Student, AdminSetting


# Create your views here.



def index(request):
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

def dashboard(request):
    if request.user.is_authenticated:
        db_name = connection.settings_dict['NAME'] # 顯示年份＝資料庫名稱
        return render(request, 'dashboard.html', {'db_name': db_name})
    else:
        return redirect('/vLogin')

def result(request):
    db_name = connection.settings_dict['NAME'] # 顯示年份＝資料庫名稱
    return render(request, 'result.html', {'db_name': db_name})

def update(request):
    db_name = connection.settings_dict['NAME'] # 顯示年份＝資料庫名稱
    return render(request, 'update.html', {'db_name': db_name})

def newYear(request):
    db_name = connection.settings_dict['NAME'] # 顯示年份＝資料庫名稱
    return render(request, 'newYear.html', {'db_name': db_name})


def upload_zip(request):
    valid_files = {'學員.csv', '課程.csv'}
    extracted_files = set()
    if request.method == 'POST' and request.FILES.get('uploadZip'):
        zip_file = request.FILES['uploadZip'] 
        fs = FileSystemStorage()
        filename = fs.save(zip_file.name, zip_file)
        file_path = fs.path(filename)
        print("filepath:" + file_path)
        print("filename:" + filename)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(fs.location)
            extracted_files = set(zip_ref.namelist())

        if not extracted_files.issubset(valid_files):
            shutil.rmtree(file_path.replace('.zip', ''), ignore_errors=False)
            fs.delete(filename)
            messages.error(request, '請依照檔名與格式要求上傳')
            print('invalid files')
            return redirect('newYear')

        for file_name in extracted_files:
            if file_name == '學員.csv':
                with open(fs.path(file_name), 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        Student.objects.create(
                            std_id=row['std_id'],
                            std_name=row['std_name'],
                            team=row['team'],
                            satb=row['satb'],
                            j_or_h=row['j_or_h'],
                            std_tag=row.get('std_tag', '')
                        )
            elif file_name == '課程.csv':
                with open(fs.path(file_name), 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        Student.objects.create(
                            std_id=row['std_id'],
                            std_name=row['std_name'],
                            team=row['team'],
                            satb=row['satb'],
                            j_or_h=row['j_or_h'],
                            std_tag=row.get('std_tag', '')
                        )

        messages.success(request, 'Upload successful!')
        print('success')
        return redirect('newYear')
    return redirect('newYear')


def stdLogout(request):
    std_logout(request)
    return redirect('/stdLogin')

def pSel(request):
    if request.session.has_key('std_id'):
        std_id = request.session['std_id']
        team = request.session['team']
        student_instance = Student.objects.get(std_id=std_id)
        team_display = Student.TEAM_CHOICES[team-1][1]
        formType = student_instance.j_or_h + str(AdminSetting.objects.get(setting_name='SelectionStage').configuration)
        form_display = dict(Student.FORM_DISPLAY)[formType]
        student = {
            'std_id': std_id , 
            'team_display': team_display, 
            'form_display': form_display,
            'std_name': student_instance.std_name,
            'formType': formType
            }  
        return render(request, 'pSel.html', {'student': student})
    else:
        return redirect('/stdLogin')
    pass