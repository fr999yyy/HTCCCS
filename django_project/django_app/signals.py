from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import AdminSetting

@receiver(post_migrate)
def create_default_admin_settings(sender, **kwargs):
    if sender.name == 'django_app':
        AdminSetting.objects.get_or_create(setting_name='SelectionStage', defaults={'configuration': '1'})
        AdminSetting.objects.get_or_create(setting_name='Junior1stRange', defaults={'configuration': '6'})
        AdminSetting.objects.get_or_create(setting_name='High1stRange', defaults={'configuration': '6'})