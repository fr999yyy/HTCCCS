from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import AdminSetting, Student

@receiver(post_migrate)
def create_default_admin_settings(sender, **kwargs):
    if sender.name == 'django_app':
        AdminSetting.objects.get_or_create(setting_name='SelectionStage', defaults={'configuration': '1'})
        AdminSetting.objects.get_or_create(setting_name='J1stRange', defaults={'configuration': '6'}) # 國中部第一次選課範圍
        AdminSetting.objects.get_or_create(setting_name='H1stRange', defaults={'configuration': '6'}) # 高中部第一次選課範圍

# @receiver(post_migrate)
# def create_default_std_Admin(sender, **kwargs):
#     if sender.name == 'django_app':
#         Student.objects.get_or_create(std_id = 998, std_name='admin', team = 1, satb = 'S', j_or_h = 'J')
#         Student.objects.get_or_create(std_id = 999, std_name='admin', team = 1, satb = 'S', j_or_h = 'H')