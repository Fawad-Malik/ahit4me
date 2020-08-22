# Generated by Django 2.1 on 2020-02-17 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('causeandeffects', '0028_auto_20200217_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='want',
            name='positive_i_want_show_more_title_2',
        ),
        migrations.AddField(
            model_name='want',
            name='steps_to_turn_positive_show_more_content_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='steps_to_turn_positive_content_1', to='causeandeffects.FirstLevelContent', verbose_name='Show More Content 1'),
        ),
        migrations.AddField(
            model_name='want',
            name='steps_to_turn_positive_show_more_content_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='steps_to_turn_positive_content_2', to='causeandeffects.FirstLevelContent', verbose_name='Show More Content 2'),
        ),
    ]
