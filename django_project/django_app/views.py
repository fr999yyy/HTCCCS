from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .auth_utils import std_authenticate, std_login, std_logout, get_student
import zipfile, csv, shutil, os
from django.core.files.storage import FileSystemStorage
from django.db import connection
from .models import Student, Section, Volunteer, Course, AdminSetting
import pandas as pd


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
    valid_files = {'db_import.xlsx'}
    if request.method == 'POST' and request.FILES.get('uploadZip'):
        zip_file = request.FILES['uploadZip']
        fs = FileSystemStorage()
        zip_filename = fs.save(zip_file.name, zip_file)
        extract_folder = fs.location + '/'
        folder_name = str(zip_file).split('.')[0] + '/'
        zip_path = fs.path(zip_filename)
        path = fs.location + '/' + folder_name
        
        # Extract the zip file into the folder
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
            extracted_files = {file.split('/')[-1] for file in zip_ref.namelist()}
        
        if extracted_files.isdisjoint(valid_files):
            shutil.rmtree(extract_folder, ignore_errors=False)
            fs.delete(zip_filename)
            messages.error(request, '請依照檔名與格式要求上傳')
            return redirect('newYear')
        
        if 'db_import.xlsx' in extracted_files:
            dfs = pd.read_excel(os.path.join(path, 'db_import.xlsx'), sheet_name=None)
            for sheet_name, df in dfs.items():
                if sheet_name == 'student':
                    for _, row in df.iterrows():
                        student_instance, created = Student.objects.get_or_create(std_id=row['std_id'])
                        print(row)
                        student_instance.std_id = row['std_id']
                        student_instance.std_name = row['std_name']
                        student_instance.team = row['team']
                        student_instance.satb = row['satb'].upper()
                        student_instance.j_or_h = row['j_or_h'].upper()
                        student_instance.std_tag = row.get('std_tag', '')
                        student_instance.save()
                elif sheet_name == 'section':
                    for _, row in df.iterrows():
                        print(row)
                        section_instance, created = Section.objects.get_or_create(section_id=row['section_id'])
                        section_instance.section_id = row['section_id']
                        section_instance.section_time = row['section_time']
                        section_instance.save()
                elif sheet_name == 'volunteer':
                    for _, row in df.iterrows():
                        print(row)
                        volunteer_instance, created = Volunteer.objects.get_or_create(volunteer_id=row['volunteer_id'])
                        volunteer_instance.volunteer_id = row['volunteer_id']
                        volunteer_instance.camp_name = row['camp_name']
                        volunteer_instance.save()
                elif sheet_name == 'course':
                    for _, row in df.iterrows():
                        print(row)
                        course_instance, created = Course.objects.get_or_create(course_id=row['course_id'])
                        course_instance.course_id = row['course_id']
                        course_instance.course_name = row['course_name']
                        course_instance.course_info = row['course_info']
                        course_instance.std_limit = 25 if pd.isna(row['std_limit']) else row['std_limit']
                        course_instance.course_type = row['course_type']
                        # Retrieve the Section instance
                        section_id = row.get('section_id')
                        if section_id:
                            section_instance = Section.objects.get(section_id=section_id)
                            course_instance.section = section_instance
                        course_instance.save()
        # Cleanup: Remove the zip file and extracted folder
        os.remove(zip_path)
        shutil.rmtree(extract_folder)
        messages.success(request, 'Upload successful!')
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