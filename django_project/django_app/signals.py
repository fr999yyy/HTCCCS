from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import AdminSetting, Student, CustomUser

@receiver(post_migrate)
def create_default_admin_settings(sender, **kwargs):
    if sender.name == 'django_app':
        AdminSetting.objects.get_or_create(setting_name='SelectionStage', defaults={'configuration': '1'})
        AdminSetting.objects.get_or_create(setting_name='J1stRange', defaults={'configuration': '6'}) # 國中部第一次選課範圍
        AdminSetting.objects.get_or_create(setting_name='H1stRange', defaults={'configuration': '6'}) # 高中部第一次選課範圍
        AdminSetting.objects.get_or_create(setting_name='select_before_camp', defaults={'configuration': True}) 

@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    if sender.name == 'django_app':
        # Create default users here
        Student.objects.get_or_create(std_id=998, std_name='admin', team=1, satb='S', j_or_h='J')
        Student.objects.get_or_create(std_id=999, std_name='admin', team=1, satb='S', j_or_h='H')
        
        # Create default users
        volunteer_user, created = CustomUser.objects.get_or_create(username='volunteer', defaults={
            'is_superuser': False,
            'is_staff': True,
            'std_id': 9999,  # Set a unique std_id
        })
        if created:
            volunteer_user.set_password('htcccs_v')
            volunteer_user.save()

        cs_user, created = CustomUser.objects.get_or_create(username='cs', defaults={
            'is_superuser': False,
            'is_staff': True,
            'std_id': 99999,  # Set a unique std_id
        })
        if created:
            cs_user.set_password('htcccs_cs')
            cs_user.save()

        admin_user, created = CustomUser.objects.get_or_create(username='admin', defaults={
            'is_superuser': True,
            'is_staff': True,
            'std_id': 999999,  # Set a unique std_id
        })
        if created:
            admin_user.set_password('HTCCcs2025')
            admin_user.save()
        # Superuser 寫在 docker-compose.yml 裡面
# @receiver(post_migrate)
# def create_default_std_Admin(sender, **kwargs):
#     if sender.name == 'django_app':
#         Student.objects.get_or_create(std_id = 998, std_name='admin', team = 1, satb = 'S', j_or_h = 'J')
#         Student.objects.get_or_create(std_id = 999, std_name='admin', team = 1, satb = 'S', j_or_h = 'H')