# Generated by Django 2.1 on 2018-08-30 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='mode',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
