from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.



class CustomUser(AbstractUser):
    std_id = models.CharField(max_length=100, unique=True)
    team = models.CharField(max_length=100)
    satb = models.CharField(max_length=100)
    
    class Meta:
        permissions = [
            ('is_student', 'Student'),
            ('is_volunteer', 'Volunteer'),
            ('is_cs', 'Course Selection'),
            ('is_admin', 'Admin'),
        ]

class Student(models.Model):
    TEAM_CHOICES = [
    (1, '第一小隊'),
    (2, '第二小隊'),
    (3, '第三小隊'),
    (4, '第四小隊'),
    (5, '第五小隊'),
    (6, '第六小隊'),
    (7, '第七小隊'),
    (8, '第八小隊'),
]

    J_OR_H_CHOICES = [
    ('J', 'Junior'),
    ('H', 'High')
]
    FORM_DISPLAY = {
        'J1' : '第一次選課｜國中部',
        'J2' : '第二次選課｜國中部',
        'H1' : '第一次選課｜高中部',
        'H2' : '第二次選課｜高中部'
    }
    std_id = models.IntegerField(primary_key=True)
    std_name = models.CharField(max_length=10, null=True)
    team = models.IntegerField(choices=TEAM_CHOICES, null=True)
    satb = models.CharField(max_length=1, choices=[('S', 'S'), ('A', 'A'), ('T', 'T'), ('B', 'B')], null=True, blank=True)
    j_or_h = models.CharField(max_length=1, choices=J_OR_H_CHOICES, null=True, blank=True)
    std_tag = models.CharField(max_length=15, blank=True, null=True)
    form1_completed = models.BooleanField(default=False)  # New field for 1st form completion
    form2_completed = models.BooleanField(default=False)  # New field for 2nd form completion

    def get_j_or_h(self):
        return self.dict(J_OR_H_CHOICES).get(j_or_h)

class Volunteer(models.Model):
    volunteer_id = models.AutoField(primary_key=True)
    camp_name = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)

class Section(models.Model):
    # 原本用於節次顯示，用節次時段表中的section_disply取代
    # SECTION_CHOICES = [
    #     ('1', '第一節'),
    #     ('2', '第二節'),
    #     ('3', '第三節'),
    #     ('4', '第四節'),
    #     ('5', '第五節'),
    #     ('6', '第六節'),
    #     ('7', '第七節'),
    #     ('8', '第八節'),
    #     ('9', '第九節'),
    #     ('10', '第十節'),
    #     ('11', '第十一節'),
    #     ('12', '第十二節'),
    #     ('13', '第十三節'),
    #     ('14', '第十四節'),
    #     ('15', '第十五節'),
    # ]

    section_id = models.AutoField(primary_key=True)
    section_time = models.CharField(max_length=30)
    section_display = models.CharField(max_length=30, default='')

    def __str__(self):
        return f"Section {self.section_id}: {self.section_time}"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    course_info = models.TextField(max_length=255, blank=True, null=True)
    std_limit = models.IntegerField(default=25)
    course_type = models.CharField(max_length=2)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    selection_results = GenericRelation('SelectionResult')


    def __str__(self):
        return self.course_name

class SpecialCourse(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    course_info = models.TextField(max_length=255, blank=True, null=True)
    std_limit = models.IntegerField(default=99)
    course_type = models.CharField(max_length=2)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.course_name

class Selection(models.Model):
    priority = models.IntegerField()
    std = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.CharField(max_length=50)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    form_type = models.CharField(max_length=2, default='J1')

class SelectionResult(models.Model):
    std = models.ForeignKey(Student, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    course = GenericForeignKey('content_type', 'object_id')
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    form_type = models.CharField(max_length=2, default='J1')

class AdminSetting(models.Model):
    setting_name = models.CharField(max_length=50, primary_key=True)
    configuration = models.CharField(max_length=50)
