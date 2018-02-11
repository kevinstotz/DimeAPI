# Generated by Django 2.0.1 on 2018-02-08 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DimeAPI', '0018_auto_20180208_1142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='fromAddress',
            new_name='fromUser',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='toAddress',
            new_name='toUser',
        ),
        migrations.AlterField(
            model_name='register',
            name='deviceInfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DimeAPI.UserAgent'),
        ),
    ]
