# Generated by Django 4.1.5 on 2023-07-23 18:58

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0013_amenities_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='listing.category'),
        ),
    ]
