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
    valid_files = {'volunteer.csv', 'course.csv', 'section.csv', 'student.csv'}
    extracted_files = set()
    if request.method == 'POST' and request.FILES.get('uploadZip'):
        zip_file = request.FILES['uploadZip'] 
        fs = FileSystemStorage()
        filename = fs.save(zip_file.name, zip_file)
        file_path = fs.path(filename)
        zip_folder = f"{fs.location}/{filename.split('.')[0]}/"
        print("filepath:" + file_path)
        print("zip_folder:" + zip_folder)
        print("filename:" + filename)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(fs.location)
            extracted_files = {file.split('/')[-1] for file in zip_ref.namelist()}
            print(extracted_files)

        if extracted_files.isdisjoint(valid_files):
            shutil.rmtree(zip_folder, ignore_errors=False)
            fs.delete(filename)
            messages.error(request, '請依照檔名與格式要求上傳')
            print('invalid files')
            return redirect('newYear')

        for file_name in extracted_files:
            if file_name == 'student.csv':
                with open(zip_folder + file_name, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        student_instance, created = Student.objects.get_or_create(std_id=row['std_id'])
                        student_instance.std_id = row['std_id']
                        student_instance.std_name = row['std_name']
                        student_instance.team = row['team']
                        student_instance.satb = row['satb'].upper()
                        student_instance.j_or_h = row['j_or_h'].upper()
                        student_instance.std_tag = row.get('std_tag', '')
                        student_instance.save()
                        print('student' + student_instance.std_id + 'saved')
            elif file_name == 'section.csv':
                with open(fs.path(file_name), 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        section_instance, created = Section.objects.get_or_create(section_id=row['section_id'])
                        section_instance.section_id = row['section_id']
                        section_instance.section_time = row['section_time']
                        section_instance.save()
                        print('section' + section_instance.section_id + 'saved')

            elif file_name == 'volunteer.csv':
                with open(fs.path(file_name), 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        volunteer_instance, created = Section.objects.get_or_create(volunteer_id=row['volunteer_id'])
                        volunteer_instance.volunteer_id=row['volunteer_id']
                        volunteer_instance.camp_name=row['camp_name']
                        volunteer_instance.save()
                        print('volunteer' + volunteer_instance.volunteer_id + 'saved')
            elif file_name == 'course.csv':
                with open(fs.path(file_name), 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        course_instance, created = Course.objects.get_or_create(course_id=row['course_id'])
                        course_instance.course_id=row['course_id']
                        course_instance.course_name=row['course_name']
                        course_instance.course_info=row['course_info']
                        course_instance.std_limit=row['std.limit']
                        course_instance.course_type=row['course_type']
                        course_instance.section=row.get('section_id')
                        course_instance.save()
                        print('course' + course_instance.course_id + 'saved')
   
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