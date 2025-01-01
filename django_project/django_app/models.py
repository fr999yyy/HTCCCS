from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.




class CustomUser(AbstractUser):
    std_id = models.IntegerField(unique=True)
    team = models.IntegerField()
    satb = models.CharField(max_length=1, choices=[('S', 'Soprano'), ('A', 'Alto'), ('T', 'Tenor'), ('B', 'Bass')])


class Student(models.Model):
    std_id = models.IntegerField(primary_key=True)
    std_name = models.CharField(max_length=50)
    team = models.IntegerField()
    satb = models.CharField(max_length=1, choices=[('S', 'Soprano'), ('A', 'Alto'), ('T', 'Tenor'), ('B', 'Bass')])
    j_or_h = models.CharField(max_length=6, choices=[('Junior', 'Junior'), ('High', 'High')])
    std_tag = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.std_name

class Volunteer(models.Model):
    volunteer_id = models.AutoField(primary_key=True)
    camp_name = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.camp_name or f"Volunteer {self.volunteer_id}"

class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_time = models.CharField(max_length=30)

    def __str__(self):
        return f"Section {self.section_id}: {self.section_time}"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50)
    course_info = models.CharField(max_length=255, blank=True, null=True)
    std_limit = models.IntegerField(blank=True, null=True)
    course_type = models.CharField(max_length=1)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name

class CourseVolunteer(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    volunteer_id = models.ForeignKey(Volunteer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course_id', 'volunteer_id')

    def __str__(self):
        return f"{self.course_id} - {self.volunteer_id}"

class Form(models.Model):
    form_id = models.AutoField(primary_key=True)
    form_type = models.CharField(
        max_length=2, 
        choices=[('J1', 'Junior Stage 1'), ('H1', 'High Stage 1'), ('J2', 'Junior Stage 2'), ('H2', 'High Stage 2')]
    )
    j_or_h = models.CharField(max_length=1, choices=[('J', 'Junior'), ('H', 'High')])
    sectionID = models.ForeignKey(Section, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Form {self.form_id}: {self.form_type}"

class Selection(models.Model):
    selection_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    priority_order = models.IntegerField()
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    def __str__(self):
        return f"Selection {self.selection_id} by {self.student}"

class AdminSetting(models.Model):
    setting_name = models.CharField(max_length=50, primary_key=True)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.setting_name}: {self.value}"

