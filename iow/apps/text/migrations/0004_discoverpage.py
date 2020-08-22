# Generated by Django 2.1 on 2019-12-05 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_auto_20190919_1853'),
        ('practice', '0034_practicesession_purpose'),
        ('text', '0003_delete_discoverpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscoverPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dream', models.CharField(max_length=350, verbose_name='Dream')),
                ('order', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discover_category', to='categories.Category', verbose_name='Category')),
                ('practice_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discover_category', to='practice.PracticeSession', verbose_name='Practice Session')),
            ],
        ),
    ]
