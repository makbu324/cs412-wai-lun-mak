# Generated by Django 5.1.2 on 2024-10-24 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0006_alter_friend_profile1_alter_friend_profile2'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]