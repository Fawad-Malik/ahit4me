# Generated by Django 2.1 on 2019-10-08 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20191008_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='ps_ismantra',
            field=models.BooleanField(default=False),
        ),
    ]
