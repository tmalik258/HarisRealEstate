# Generated by Django 4.1.5 on 2023-07-17 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_trafficuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trafficuser',
            options={'ordering': ('-time_created',), 'verbose_name': 'Traffic User', 'verbose_name_plural': 'Traffic Users'},
        ),
    ]