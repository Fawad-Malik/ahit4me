# Generated by Django 2.1 on 2019-11-15 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('causeandeffects', '0014_obstaclestocomplete_opportunitiestochange_whatincreasesability_worldclassability'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='whatincreasesability',
            options={'verbose_name': 'What Increases Ability', 'verbose_name_plural': 'What Increases Abilities'},
        ),
        migrations.AlterModelOptions(
            name='worldclassability',
            options={'verbose_name': 'World Class Ability', 'verbose_name_plural': 'World Class Abilities'},
        ),
    ]
