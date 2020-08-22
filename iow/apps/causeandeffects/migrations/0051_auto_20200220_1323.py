# Generated by Django 2.1 on 2020-02-20 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('causeandeffects', '0050_auto_20200220_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s1_l2_f1_header_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 1: 2nd Level: 1st Field: Header Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s1_l2_f2_header_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 1: 2nd Level: 2nd Field: Header Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s1_l2_f3_header_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 1: 2nd Level: 3rd Field: Header Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s1_l3_button1_text',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 1: 3rd Level: First Button Text'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s1_l3_button2_text',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 1: 3rd Level: Second Button Text'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s1_l3_button3_text',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 1: 3rd Level: Third Button Text'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s1_l3_f1_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 1: 3rd Level: First Field Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s1_l3_f2_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 1: 3rd Level: Second Field Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s1_l3_f3_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 1: 3rd Level: Third Field Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s2_l2_f1_header_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 2: 2nd Level: 1st Field: Header Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s2_l2_f2_header_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 2: 2nd Level: 2nd Field: Header Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s2_l2_f3_header_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 2: 2nd Level: 3rd Field: Header Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s2_l3_button1_text',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 2: 3rd Level: First Button Text'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s2_l3_button2_text',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 2: 3rd Level: Second Button Text'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s2_l3_button3_text',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 2: 3rd Level: Third Button Text'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s2_l3_f1_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 2: 3rd Level: First Field Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s2_l3_f2_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 2: 3rd Level: Second Field Title'),
        ),
        migrations.AddField(
            model_name='settings',
            name='habitats_outside_of_me_s2_l3_f3_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section 2: 3rd Level: Third Field Title'),
        ),
    ]
