# Generated by Django 2.0.1 on 2018-02-16 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DimeAPI', '0046_auto_20180215_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimemutualfund',
            name='available_supply',
            field=models.BigIntegerField(default=0),
        ),
    ]
