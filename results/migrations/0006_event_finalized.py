# Generated by Django 5.2.1 on 2025-05-15 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0005_alter_event_major_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='finalized',
            field=models.BooleanField(default=False, help_text='Mark this event as finalized to lock stats and show medals.'),
        ),
    ]
