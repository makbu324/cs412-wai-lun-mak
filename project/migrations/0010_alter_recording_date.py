# Generated by Django 5.1.3 on 2024-12-01 04:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_alter_recording_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
