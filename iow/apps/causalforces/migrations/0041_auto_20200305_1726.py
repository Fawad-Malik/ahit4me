# Generated by Django 2.1 on 2020-03-05 12:26

from django.db import migrations, models
import django.db.models.deletion
import iow.apps.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('causalforces', '0040_auto_20200305_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='BehaviorPeople',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(default=iow.apps.core.models.create_default_hash, editable=False, max_length=30)),
                ('idate', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('udate', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('name', models.CharField(max_length=250, verbose_name='BehaviorSelf')),
                ('current_behavior', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='behaviorpeople_behavior', to='causalforces.Behavior')),
            ],
            options={
                'verbose_name_plural': 'BehaviorPeoples',
                'verbose_name': 'BehaviorPeople',
            },
        ),
        migrations.AddField(
            model_name='userbehavior',
            name='behaviorpeople',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_behaviorpeople', to='causalforces.BehaviorPeople'),
        ),
    ]
