# Generated by Django 2.1 on 2019-09-24 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0026_auto_20190917_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='affirmationtext',
            name='repeat',
            field=models.BooleanField(default=False, verbose_name='Repeat'),
        ),
    ]
