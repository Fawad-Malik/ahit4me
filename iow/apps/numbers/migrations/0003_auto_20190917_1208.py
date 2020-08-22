# Generated by Django 2.1 on 2019-09-17 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('numbers', '0002_auto_20190917_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstats',
            name='practice_session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ps_stats', to='practice.PracticeSession'),
        ),
        migrations.AlterField(
            model_name='userstats',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_stats', to=settings.AUTH_USER_MODEL),
        ),
    ]
