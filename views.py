import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .models import SelectionResult, Student, Course, Section

def process_excel_form(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            std_id = row['std_id']
            student = Student.objects.get(std_id=std_id)
            for section_id, course_name in row.items():
                if section_id != 'std_id':
                    section = Section.objects.get(section_id=section_id)
                    course = Course.objects.get(name=course_name, section=section)
                    SelectionResult.objects.create(std=student, course=course)

        return render(request, 'success.html')

    return render(request, 'upload_excel.html')