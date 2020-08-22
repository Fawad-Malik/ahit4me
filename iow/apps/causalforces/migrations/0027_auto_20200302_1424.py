# Generated by Django 2.1 on 2020-03-02 09:24

from django.db import migrations, models
import django.db.models.deletion
import iow.apps.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('causalforces', '0026_life_userlife'),
    ]

    operations = [
        migrations.CreateModel(
            name='BehaviorLife',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(default=iow.apps.core.models.create_default_hash, editable=False, max_length=30)),
                ('idate', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('udate', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('name', models.CharField(max_length=250, verbose_name='Life')),
                ('current_behavior', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='life_behavior', to='causalforces.Behavior')),
            ],
            options={
                'verbose_name': 'BehaviorLife',
                'verbose_name_plural': 'BehaviorLifes',
            },
        ),
        migrations.RemoveField(
            model_name='userlife',
            name='thought',
        ),
        migrations.DeleteModel(
            name='UserLife',
        ),
    ]
