# Generated by Django 2.0.1 on 2018-02-28 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DimeAPI', '0066_auto_20180221_1746'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dimehistory',
            unique_together={('time', 'xchange')},
        ),
    ]
