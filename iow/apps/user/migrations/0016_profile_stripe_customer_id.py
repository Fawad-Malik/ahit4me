# Generated by Django 2.1 on 2019-11-27 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_usersettings_ps_ismantra'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripe_customer_id',
            field=models.CharField(default='', max_length=200),
        ),
    ]
