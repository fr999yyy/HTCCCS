from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import AdminSetting, Student
from django.contrib.auth.models import User

@receiver(post_migrate)
def create_default_admin_settings(sender, **kwargs):
    if sender.name == 'django_app':
        AdminSetting.objects.get_or_create(setting_name='SelectionStage', defaults={'configuration': '1'})
        AdminSetting.objects.get_or_create(setting_name='J1stRange', defaults={'configuration': '6'}) # 國中部第一次選課範圍
        AdminSetting.objects.get_or_create(setting_name='H1stRange', defaults={'configuration': '6'}) # 高中部第一次選課範圍
        AdminSetting.objects.get_or_create(setting_name='select_before_camp', defaults={'configuration': True}) 

def create_default_users(sender, **kwargs):
    if sender.name == 'django_app':
        # Create default users here
        Student.objects.get_or_create(std_id=998, std_name='admin', team=1, satb='S', j_or_h='J')
        Student.objects.get_or_create(std_id=999, std_name='admin', team=1, satb='S', j_or_h='H')
        Student.objects.get_or_create(std_id=1000, std_name='admin', team=1, satb='S', j_or_h='J')
        User.objects.get_or_create(username='volunteer', password='htcccs_v', is_superuser=False, is_staff=True)
        User.objects.get_or_create(username='cs', password='htccCS', is_superuser=False, is_staff=True)
        # Superuser 寫在 docker-compose.yml 裡面
# @receiver(post_migrate)
# def create_default_std_Admin(sender, **kwargs):
#     if sender.name == 'django_app':
#         Student.objects.get_or_create(std_id = 998, std_name='admin', team = 1, satb = 'S', j_or_h = 'J')
#         Student.objects.get_or_create(std_id = 999, std_name='admin', team = 1, satb = 'S', j_or_h = 'H')