# Generated by Django 2.0.1 on 2018-02-15 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DimeAPI', '0042_auto_20180215_1226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cryptocomparecoins',
            old_name='dime_coin',
            new_name='local_coin',
        ),
    ]
