from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class CustomUser(AbstractUser):
    std_id = models.CharField(max_length=100, unique=True)
    team = models.CharField(max_length=100)
    satb = models.CharField(max_length=100)

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
    std_name = models.CharField(max_length=10)
    team = models.IntegerField(choices=TEAM_CHOICES)
    satb = models.CharField(max_length=1, choices=[('S', 'S'), ('A', 'A'), ('T', 'T'), ('B', 'B')])
    j_or_h = models.CharField(max_length=1, choices=J_OR_H_CHOICES)
    std_tag = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.std_name
    def get_j_or_h(self):
        return self.dict(J_OR_H_CHOICES).get(j_or_h)


class AdminSetting(models.Model):
    setting_name = models.CharField(max_length=50, primary_key=True)
    configuration = models.CharField(max_length=50)
