# Generated by Django 4.1.5 on 2023-07-30 21:05

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0014_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=mptt.fields.TreeForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='listing.category'),
        ),
    ]