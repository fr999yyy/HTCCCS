from django.contrib.auth.backends import BaseBackend
from django_app.models import Students

# class CustomAuthBackend(BaseBackend):
#     def authenticate(self, request, std_id=None, team=None, satb=None):
#         try:
#             students = Students.objects.get(std_id=std_id, team=team, satb=satb)
#             return students
#         except Students.DoesNotExist:
#             return None

#     def get_student(self, std_id):
#         try:
#             return Students.objects.get(pk=std_id)
#         except Students.DoesNotExist:
#             return None