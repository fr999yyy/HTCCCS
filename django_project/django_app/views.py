from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .auth_utils import std_authenticate, std_login, std_logout, get_student
import zipfile, csv, shutil, os
from django.core.files.storage import FileSystemStorage
from django.db import connection
from .models import Student, Section, Volunteer, Course, AdminSetting, Selection, SpecialCourse
import pandas as pd


# Create your views here.



def index(request):
    return render(request, 'index.html')

def stdLogin(request):
    if request.session.has_key('std_id'):
            return redirect('/pSel')
    if request.method == 'POST':
        if not request.POST['std_id'] or not request.POST['team'] or not request.POST['satb']:
            messages.error(request, '請填寫所有欄位')
            return redirect('/stdLogin')
        std_id = request.POST['std_id']
        team = request.POST['team']
        satb = request.POST['satb']
        current_form = AdminSetting.objects.get(setting_name='SelectionStage').configuration
        print(std_id, team, satb)
        student = std_authenticate(std_id=std_id, team=team, satb=satb)
        student_instance = Student.objects.get(std_id=std_id)
        if student_instance.form1_completed & (current_form == 1):
            messages.error(request, '你已經選過課囉！')
            return redirect('/stdLogin')
        if student_instance.form2_completed & (current_form == 2):
            messages.error(request, '你已經選過課囉！')
            return redirect('/stdLogin')


        if student is not None:
            std_login(request, student)
            print('login success')
            return redirect ('/pSel')
        else:
            messages.info(request, '無法登入，請檢查資料是否正確')
            print('login failed')
            return redirect('/stdLogin')
    else:
        return render(request, 'stdLogin.html')

def vLogin(request):
    # if request.user.is_authenticated:
    #     return redirect('/dashboard')
    if request.method == 'POST':
        if not request.POST['password']:
            messages.error(request, '請輸入密碼')
            return redirect('/vLogin')
        password = request.POST['password']

        user = auth.authenticate(username='admin', password=password)

        if user is not None:
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
    valid_files = {'db_import.xlsx', 'pfp'}
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
                        # print(row)
                        student_instance.std_id = row['std_id']
                        student_instance.std_name = row['std_name']
                        student_instance.team = row['team']
                        student_instance.satb = row['satb'].upper()
                        student_instance.j_or_h = row['j_or_h'].upper()
                        student_instance.std_tag = row.get('std_tag', '')
                        student_instance.save()
                elif sheet_name == 'section':
                    for _, row in df.iterrows():
                        # print(row)
                        section_instance, created = Section.objects.get_or_create(section_id=row['section_id'])
                        section_instance.section_id = row['section_id']
                        section_instance.section_time = row['section_time']
                        section_instance.section_display = row['section_display']
                        section_instance.save()
                elif sheet_name == 'volunteer':
                    for _, row in df.iterrows():
                        # print(row)
                        volunteer_instance, created = Volunteer.objects.get_or_create(volunteer_id=row['volunteer_id'])
                        volunteer_instance.volunteer_id = row['volunteer_id']
                        volunteer_instance.camp_name = row['camp_name']
                        volunteer_instance.save()
                elif sheet_name == 'course':
                    for _, row in df.iterrows():
                        # print(row)
                        if row['course_type'] == 'js' or row['course_type'] == 'hs':
                            course_instance, created = SpecialCourse.objects.get_or_create(course_id=row['course_id'])
                            course_instance.std_limit = 99 if pd.isna(row['std_limit']) else row['std_limit']
                        else:
                            course_instance, created = Course.objects.get_or_create(course_id=row['course_id'])
                            course_instance.std_limit = 25 if pd.isna(row['std_limit']) else row['std_limit']
                        course_instance.course_id = row['course_id']
                        course_instance.course_name = row['course_name']
                        course_instance.course_info = row['course_info'] if pd.notna(row['course_info']) else '無課程資訊'
                        course_instance.course_type = row['course_type'].upper()
                        # Retrieve the Section instance
                        section_id = row.get('section_id')
                        course_instance.section_id = Section.objects.get(section_id=section_id)
                        course_instance.save()
        # Cleanup: Remove the zip file and extracted folder
        os.remove(zip_path)
        # shutil.rmtree(path)
        messages.success(request, '資料匯入已完成')
        return redirect('newYear')
    return redirect('newYear')


def pSel(request):
    if request.session.has_key('std_id'):
        std_id = request.session['std_id']
        team = request.session['team']
        student_instance = Student.objects.get(std_id=std_id)
        team_display = Student.TEAM_CHOICES[team-1][1]
        current_form = AdminSetting.objects.get(setting_name='SelectionStage').configuration
        form_type = student_instance.j_or_h + str(current_form) #returning J1, J2, H1, H2
        form_display = dict(Student.FORM_DISPLAY)[form_type] #returning 第一次選課｜國中部, 第二次選課｜國中部, 第一次選課｜高中部, 第二次選課｜高中部
        
        student = {
            'std_id': std_id,
            'team_display': team_display,
            'form_display': form_display,
            'std_name': student_instance.std_name
        }
        request.session['team_display'] = team_display
        request.session['form_display'] = form_display
        request.session['current_form'] = current_form
        return render(request, 'pSel.html', {'student': student, 'team_display': team_display, 'form_display': form_display})
    else:
        return redirect('/stdLogin')
    pass

def get_courses(request):
    std_id = request.session['std_id']
    student_instance = Student.objects.get(std_id=std_id)
    selection_range = AdminSetting.objects.get(setting_name=student_instance.j_or_h + '1stRange').configuration
    section_instances = Section.objects.filter(section_id__lte=selection_range)
    course_instances = Course.objects.filter(section_id__lte=selection_range, course_type__in=[student_instance.j_or_h, 'M'])
    sp_course_instances = SpecialCourse.objects.filter(section_id__lte=selection_range, course_type=student_instance.j_or_h+'S') # 'JS'國中部課程, 'HS'高中部課程
    
    sections_with_courses = [] # list中插入dict用來分開儲存每一個節次對應的所有課程，以及課程數量，用來顯示志願選項數量
    for section in section_instances:
        courses_in_section = []
        sp_courses_in_section = sp_course_instances.filter(section_id=section.section_id)
        if sp_courses_in_section.exists():
            for course in sp_courses_in_section:
                if '_' in course.course_name:
                    if '、' in course.course_name:
                        teachers =  course.course_name.split('_')[1].split('、') 
                    else:
                        teachers = [course.course_name.split('_')[1]]
                else: teachers = []
                print("老師："+str(teachers))
                courses_in_section.append({
                    'course_id': course.course_id,
                    'course_name': course.course_name,
                    'course_info': course.course_info,
                    'teachers': teachers
                })
        else:
            for course in course_instances.filter(section_id=section.section_id):
                if '_' in course.course_name:
                    if '、' in course.course_name:
                        teachers =  course.course_name.split('_')[1].split('、') 
                    else:
                        teachers = [course.course_name.split('_')[1]]
                else: teachers = []
                print("老師："+str(teachers))
                courses_in_section.append({
                    'course_id': course.course_id,
                    'course_name': course.course_name,
                    'course_info': course.course_info,
                    'teachers': teachers
                })
        num_courses = len(courses_in_section)
        sections_with_courses.append({
            'section_id': section.section_id,
            'section_time': section.section_time,
            'section_display': section.section_display,
            'courses': courses_in_section,
            'num_courses': num_courses
        })

    return JsonResponse({'sections_with_courses': sections_with_courses})

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Student, Section, Course, AdminSetting

def double_check(request): # merge with confirm
    if request.method == 'POST':
        selections = request.POST.getlist('priority')
        std_id = request.session['std_id']
        # Temporarily save the user's choices in the session
        request.session['selections'] = selections
        # print('selections:', selections)
        return redirect('confirm')

    return redirect('pSel')

def confirm(request):
    team_display = request.session['team_display']
    form_display = request.session['form_display']
    selections = request.session.get('selections', [])
    std_id = request.session['std_id']
    student = Student.objects.get(std_id=std_id)

    # Process selections to generate the table data
    table_data = {}
    priorities = set()

    for selection in selections:
        priority, course_id, std_id, section_id = selection.split('-')
        if SpecialCourse.objects.filter(course_id=course_id).exists():
            course = SpecialCourse.objects.get(course_id=course_id)
        else:
            course = Course.objects.get(course_id=course_id)
        section = Section.objects.get(section_id=section_id)
        if section.section_display not in table_data:
            table_data[section.section_display] = {}
        table_data[section.section_display][priority] = course.course_name
        priorities.add(priority)


    # Sort priorities
    sorted_priorities = sorted(priorities, key=int)

    return render(request, 'confirm.html', {
        'student': student,
        'table_data': table_data,
        'sorted_priorities': sorted_priorities,
        'team_display': team_display,
        'form_display': form_display,
    })

def submit_form(request):
    selections = request.session.get('selections', [])
    std_id = request.session['std_id']  # Assuming std_id is used as the username

    # Process and save the selections to the database
    for selection in selections:
        priority, course_id, std_id, section_id = selection.split('-')

        if SpecialCourse.objects.filter(course_id=course_id).exists():
            course_instance = SpecialCourse.objects.get(course_id=course_id)
        else:
            course_instance = Course.objects.get(course_id=course_id)

        selection_instance = Selection.objects.create(
            priority=priority,
            std_id=Student.objects.get(std_id=std_id),
            course_id=course_instance.course_id,
            section_id=Section.objects.get(section_id=section_id)
        )

    # Clear the selections from the session
    del request.session['selections']
    return redirect('success')  # Redirect to a success page or another appropriate page

def success(request):
    std_id = request.session['std_id']
    student = Student.objects.get(std_id=std_id)
    current_form = AdminSetting.objects.get(setting_name='SelectionStage').configuration


    if current_form == '1':
        student.form1_completed = True
        print('form1 completed')
    elif current_form == '2':
        student.form2_completed = True
        print('form1 completed')
    # student.save() 測試先關掉
    std_logout(request)
    return render(request, 'success.html')

def stdLogout(request):
    std_logout(request)
    return redirect('/stdLogin')