# Generated by Django 2.1 on 2019-11-27 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_profile_stripe_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='stripe_customer_id',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
