# Generated by Django 2.1 on 2020-04-16 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_auto_20200416_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_subscription',
            name='ustripe_subscription_plan',
            field=models.CharField(default='', max_length=60),
        ),
    ]
