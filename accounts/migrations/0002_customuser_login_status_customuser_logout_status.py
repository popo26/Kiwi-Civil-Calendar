# Generated by Django 4.1.1 on 2022-09-12 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='login_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='logout_status',
            field=models.BooleanField(default=False),
        ),
    ]
