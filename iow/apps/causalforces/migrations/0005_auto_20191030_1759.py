# Generated by Django 2.1 on 2019-10-30 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('causalforces', '0004_auto_20191030_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='am_i_appreciating',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Am I Appreciating'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='daily_minutes_for_caring',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Daily Minutes caring for'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='dmp_flow_habitats',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Daily Minutes Practicing'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='dmp_identify_habitats',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Daily Minutes Practicing'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='future_project',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Would I like to select as future project'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='identity_habitat',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Identify Habitat'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='is_place_card_for',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Is Place Cared for'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='pct_flow_negative',
            field=models.IntegerField(blank=True, null=True, verbose_name='% Negative Flow to Sit & Stress'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='pct_flow_neutral',
            field=models.IntegerField(blank=True, null=True, verbose_name='% Neutral Flow to Be OK'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='pct_flow_positive',
            field=models.IntegerField(blank=True, null=True, verbose_name='% Positive Flow to Want to Act'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='pct_mindful_negative',
            field=models.IntegerField(blank=True, null=True, verbose_name='% mindful Negative clear'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='pct_mindful_neutral',
            field=models.IntegerField(blank=True, null=True, verbose_name='% mindful Neutral clear'),
        ),
        migrations.AlterField(
            model_name='useridentifyhabitatsyoulivein',
            name='pct_mindful_positive',
            field=models.IntegerField(blank=True, null=True, verbose_name='% mindful positive clear'),
        ),
    ]
