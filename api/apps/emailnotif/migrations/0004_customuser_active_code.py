# Generated by Django 4.2.5 on 2023-09-11 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailnotif', '0003_alter_customuser_family_alter_customuser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='active_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
