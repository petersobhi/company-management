# Generated by Django 2.1 on 2018-08-29 01:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('company', '0003_auto_20180829_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='description',
            field=models.TextField(default='Lorem ipsum', max_length=500),
            preserve_default=False,
        ),
    ]
