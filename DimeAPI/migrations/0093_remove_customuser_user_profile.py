# Generated by Django 2.0.1 on 2018-03-08 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DimeAPI', '0092_auto_20180308_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_profile',
        ),
    ]
