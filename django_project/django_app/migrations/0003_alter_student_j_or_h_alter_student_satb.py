# Generated by Django 4.2.17 on 2025-01-18 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0002_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='j_or_h',
            field=models.CharField(blank=True, choices=[('J', 'Junior'), ('H', 'High')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='satb',
            field=models.CharField(blank=True, choices=[('S', 'S'), ('A', 'A'), ('T', 'T'), ('B', 'B')], max_length=1, null=True),
        ),
    ]
