from django.shortcuts import redirect
from django.contrib import messages
from .models import Students

def std_authenticate(std_id, team, satb):
    try:
        student = Students.objects.get(std_id=std_id, team=team, satb=satb)
        return student
    except Students.DoesNotExist:
        return None

def get_student(std_id):
    try:
        return Students.objects.get(pk=std_id)
    except Students.DoesNotExist:
        return None

def std_login(request, student):
    request.session['std_id'] = student.std_id
    request.session['team'] = student.team
    request.session['satb'] = student.satb

def std_logout(request):
    request.session.flush()