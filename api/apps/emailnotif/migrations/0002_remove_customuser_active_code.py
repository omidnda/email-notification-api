# Generated by Django 4.2.5 on 2023-09-10 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailnotif', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='active_code',
        ),
    ]
