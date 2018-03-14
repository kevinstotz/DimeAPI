# Generated by Django 2.0.1 on 2018-01-29 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DimeAPI', '0006_auto_20180129_0903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='period',
            name='period',
        ),
        migrations.AddField(
            model_name='period',
            name='day',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='period',
            name='month',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='period',
            name='quarter',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='period',
            name='year',
            field=models.IntegerField(default=2017),
        ),
    ]
