# Generated by Django 4.2.17 on 2025-01-03 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0005_section_section_display'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='section',
            new_name='section_id',
        ),
        migrations.RenameField(
            model_name='selection',
            old_name='course',
            new_name='course_id',
        ),
        migrations.RenameField(
            model_name='selection',
            old_name='student',
            new_name='student_id',
        ),
    ]
