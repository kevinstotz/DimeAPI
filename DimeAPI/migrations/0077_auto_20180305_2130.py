# Generated by Django 2.0.1 on 2018-03-05 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DimeAPI', '0076_delete_period'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passwordreset',
            old_name='authorizationCode',
            new_name='authorization_code',
        ),
    ]
