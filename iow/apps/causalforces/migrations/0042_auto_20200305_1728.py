# Generated by Django 2.1 on 2020-03-05 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('causalforces', '0041_auto_20200305_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='behaviorpeople',
            name='name',
            field=models.CharField(max_length=250, verbose_name='BehaviorPeople'),
        ),
    ]
