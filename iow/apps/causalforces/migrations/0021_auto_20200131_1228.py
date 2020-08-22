# Generated by Django 2.1 on 2020-01-31 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('causalforces', '0020_auto_20200120_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercr',
            name='am_i_appreciating_intensity',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Am I Appreciating this Place? Intensity'),
        ),
        migrations.AddField(
            model_name='usercr',
            name='body_appreciating',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Body Ability Appreciating'),
        ),
        migrations.AddField(
            model_name='usercr',
            name='body_appreciating_intensity',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Body Ability Appreciating Intensity'),
        ),
        migrations.AddField(
            model_name='usercr',
            name='body_cared_for',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Body Ability Cared For'),
        ),
        migrations.AddField(
            model_name='usercr',
            name='body_cared_for_intensity',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Body Ability Cared For Intensity'),
        ),
        migrations.AddField(
            model_name='usercr',
            name='cared_for_intensity',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Is this place Cared for? Intensity'),
        ),
        migrations.AddField(
            model_name='usercr',
            name='conscious_appreciating',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Conscious Ability Appreciating'),
        ),
        migrations.AddField(
            model_name='usercr',
            name='conscious_appreciating_intensity',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Conscious Ability Appreciating Intensity'),
        ),
        migrations.AddField(
            model_name='usercr',
            name='conscious_cared_for',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Conscious Ability Cared For'),
        ),
        migrations.AddField(
            model_name='usercr',
            name='conscious_cared_for_intensity',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Conscious Ability Cared For Intensity'),
        ),
    ]
