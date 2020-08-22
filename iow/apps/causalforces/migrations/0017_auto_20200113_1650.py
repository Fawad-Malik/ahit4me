# Generated by Django 2.1 on 2020-01-13 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('causalforces', '0016_auto_20200113_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='behaviorhighintensity',
            name='money',
            field=models.CharField(max_length=250, verbose_name='Money'),
        ),
        migrations.AlterField(
            model_name='behaviorhighintensity',
            name='people',
            field=models.CharField(max_length=250, verbose_name='People'),
        ),
        migrations.AlterField(
            model_name='behaviorhighintensity',
            name='self',
            field=models.CharField(max_length=250, verbose_name='Self'),
        ),
        migrations.AlterField(
            model_name='behaviorlowintensity',
            name='money',
            field=models.CharField(max_length=250, verbose_name='Money'),
        ),
        migrations.AlterField(
            model_name='behaviorlowintensity',
            name='people',
            field=models.CharField(max_length=250, verbose_name='People'),
        ),
        migrations.AlterField(
            model_name='behaviorlowintensity',
            name='self',
            field=models.CharField(max_length=250, verbose_name='Self'),
        ),
        migrations.AlterField(
            model_name='behaviormediumintensity',
            name='money',
            field=models.CharField(max_length=250, verbose_name='Money'),
        ),
        migrations.AlterField(
            model_name='behaviormediumintensity',
            name='people',
            field=models.CharField(max_length=250, verbose_name='People'),
        ),
        migrations.AlterField(
            model_name='behaviormediumintensity',
            name='self',
            field=models.CharField(max_length=250, verbose_name='Self'),
        ),
        migrations.AlterField(
            model_name='thoughthighintensity',
            name='money',
            field=models.CharField(max_length=250, verbose_name='Money'),
        ),
        migrations.AlterField(
            model_name='thoughthighintensity',
            name='people',
            field=models.CharField(max_length=250, verbose_name='People'),
        ),
        migrations.AlterField(
            model_name='thoughthighintensity',
            name='self',
            field=models.CharField(max_length=250, verbose_name='Self'),
        ),
        migrations.AlterField(
            model_name='thoughtlowintensity',
            name='money',
            field=models.CharField(max_length=250, verbose_name='Money'),
        ),
        migrations.AlterField(
            model_name='thoughtlowintensity',
            name='people',
            field=models.CharField(max_length=250, verbose_name='People'),
        ),
        migrations.AlterField(
            model_name='thoughtlowintensity',
            name='self',
            field=models.CharField(max_length=250, verbose_name='Self'),
        ),
        migrations.AlterField(
            model_name='thoughtmediumintensity',
            name='money',
            field=models.CharField(max_length=250, verbose_name='Money'),
        ),
        migrations.AlterField(
            model_name='thoughtmediumintensity',
            name='people',
            field=models.CharField(max_length=250, verbose_name='People'),
        ),
        migrations.AlterField(
            model_name='thoughtmediumintensity',
            name='self',
            field=models.CharField(max_length=250, verbose_name='Self'),
        ),
    ]
