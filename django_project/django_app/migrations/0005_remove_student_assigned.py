# Generated by Django 4.2.17 on 2025-05-28 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0004_student_assigned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='assigned',
        ),
    ]
