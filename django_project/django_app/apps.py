from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import models



class DjangoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app'

    def ready(self):
        import django_app.signals
        from django_app.models import AdminSetting
        # Function to create AdminSetting after migration
        def create_default_adminsetting(sender, **kwargs):
            if not AdminSetting.objects.exists():
                AdminSetting.objects.create(setting_name="select_before_camp", setting_value=True)

        # Connect to post_migrate signal to run after migrations
        post_migrate.connect(create_default_adminsetting, sender=self)