from django.shortcuts import redirect
from django.contrib import messages
from .models import Student

def std_authenticate(std_id, std_name):
    print(f"Looking for student with ID={std_id} and Name={std_name}")
    try:
        student = Student.objects.get(std_id=std_id, std_name=std_name)
        return student
    except Student.DoesNotExist:
        return None
    except Exception as e:
        print(f"Unexpected error during authentication: {e}")
        return None

def get_student(std_id):
    try:
        return Student.objects.get(std_id=std_id)
    except Student.DoesNotExist:
        return None

def std_login(request, student):
    request.session['std_id'] = student.std_id
    request.session['team'] = student.team
    request.session['std_name'] = student.std_name
    request.session['JorH'] = student.j_or_h

def std_logout(request):
    request.session.flush()