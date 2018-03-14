# Generated by Django 2.0.1 on 2018-03-07 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DimeAPI', '0084_auto_20180307_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address1', models.CharField(max_length=255, verbose_name='Address 1')),
                ('address2', models.CharField(max_length=255, verbose_name='Address 3')),
                ('address3', models.CharField(max_length=255, verbose_name='Address 2')),
                ('unit', models.CharField(max_length=20, verbose_name='Unit')),
                ('city', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='DimeAPI.City')),
                ('country', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='DimeAPI.Country')),
                ('state', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='DimeAPI.State')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('zipcode', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='DimeAPI.ZipCode')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
