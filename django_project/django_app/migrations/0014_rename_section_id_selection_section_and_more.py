# Generated by Django 4.2.17 on 2025-01-08 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0013_alter_selection_form_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='selection',
            old_name='section_id',
            new_name='section',
        ),
        migrations.RenameField(
            model_name='selection',
            old_name='std_id',
            new_name='std',
        ),
    ]
