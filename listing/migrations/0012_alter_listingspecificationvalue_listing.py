# Generated by Django 4.1.5 on 2023-07-18 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0011_remove_listing_area_size_remove_listing_purpose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingspecificationvalue',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specification_value', to='listing.listing'),
        ),
    ]
