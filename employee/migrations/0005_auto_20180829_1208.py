# Generated by Django 2.1 on 2018-08-29 12:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('employee', '0004_employee_job_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='job_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
