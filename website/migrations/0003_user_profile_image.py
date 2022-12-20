# Generated by Django 4.1.3 on 2022-12-06 07:44

from django.db import migrations, models
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_user_bio_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to=website.models.User.user_directory_path),
        ),
    ]
