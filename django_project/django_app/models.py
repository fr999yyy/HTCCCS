from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class CustomUser(AbstractUser):
    std_id = models.CharField(max_length=100, unique=True)
    team = models.CharField(max_length=100)
    satb = models.CharField(max_length=100)

class Students(models.Model):
    std_id = models.IntegerField(primary_key=True)
    std_name = models.CharField(max_length=10)
    team = models.IntegerField()
    satb = models.CharField(max_length=1, choices=[('S', 'S'), ('A', 'A'), ('T', 'T'), ('B', 'B')])
    j_or_h = models.CharField(max_length=1, choices=[('J', 'Junior'), ('H', 'High')])
    std_tag = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.std_name
        return self.team