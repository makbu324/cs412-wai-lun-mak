# Generated by Django 5.1.3 on 2024-11-30 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_remove_song_added_by_user_artist_image_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chord',
            name='audio_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='chord',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
