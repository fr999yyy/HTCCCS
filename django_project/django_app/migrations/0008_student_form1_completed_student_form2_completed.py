# Generated by Django 4.2.17 on 2025-01-06 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0007_rename_student_id_selection_std_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='form1_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='form2_completed',
            field=models.BooleanField(default=False),
        ),
    ]
