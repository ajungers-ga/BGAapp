# Generated by Django 5.2.1 on 2025-05-15 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_player_accolades_player_hof_inducted_player_hof_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='career_events_played',
        ),
        migrations.RemoveField(
            model_name='player',
            name='career_wins',
        ),
    ]
