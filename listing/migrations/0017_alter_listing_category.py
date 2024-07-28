# Generated by Django 4.1.5 on 2023-07-30 21:40

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0016_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=mptt.fields.TreeForeignKey(default='House', on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='listing.category'),
        ),
    ]
