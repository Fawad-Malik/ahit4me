# Generated by Django 2.1 on 2019-10-22 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import iow.apps.core.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('causeandeffects', '0004_auto_20191022_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(default=iow.apps.core.models.create_default_hash, editable=False, max_length=30)),
                ('idate', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('udate', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='why_want_user', to=settings.AUTH_USER_MODEL)),
                ('why_want', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_why_wants', to='causeandeffects.WhyWant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
