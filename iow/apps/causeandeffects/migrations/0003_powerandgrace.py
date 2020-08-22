# Generated by Django 2.1 on 2019-10-22 05:20

from django.db import migrations, models
import django.db.models.deletion
import iow.apps.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('causeandeffects', '0002_want_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='PowerAndGrace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(default=iow.apps.core.models.create_default_hash, editable=False, max_length=30)),
                ('idate', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('udate', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('ability', models.CharField(max_length=200, verbose_name='Ability')),
                ('want', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='want_power_and_grace', to='causeandeffects.Want')),
            ],
            options={
                'verbose_name_plural': 'Power & Grace Abilities',
                'verbose_name': 'Power & Grace Ability',
            },
        ),
    ]
