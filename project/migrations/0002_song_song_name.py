# Generated by Django 5.1.3 on 2024-11-22 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='song_name',
            field=models.TextField(blank=True),
        ),
    ]
