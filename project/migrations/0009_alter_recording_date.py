# Generated by Django 5.1.3 on 2024-12-01 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_recording_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]