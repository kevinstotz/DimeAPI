# Generated by Django 2.0.1 on 2018-03-07 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DimeAPI', '0083_auto_20180307_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='code',
            field=models.CharField(default='XX', max_length=2, verbose_name='State Code'),
        ),
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(default='XX', max_length=40, verbose_name='State Name'),
        ),
    ]
