# Generated by Django 4.1.5 on 2023-07-17 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_profile_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrafficUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=256, verbose_name='User Ip Address')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-time_created',),
            },
        ),
    ]