# Generated by Django 5.1.2 on 2024-10-24 17:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0005_friend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='profile1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile1', to='mini_fb.profile'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='profile2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile2', to='mini_fb.profile'),
        ),
    ]