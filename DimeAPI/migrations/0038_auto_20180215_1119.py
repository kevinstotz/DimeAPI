# Generated by Django 2.0.1 on 2018-02-15 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DimeAPI', '0037_remove_cryptocomparecoins_min_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocomparecoins',
            name='id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
    ]
