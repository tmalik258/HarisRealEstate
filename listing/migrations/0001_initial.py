# Generated by Django 4.1.5 on 2023-07-11 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import listing.models
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=24)),
                ('lname', models.CharField(blank=True, max_length=24)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('price', models.IntegerField()),
                ('purpose', models.CharField(choices=[('S', 'Sale'), ('R', 'Rent Out')], default='S', max_length=2)),
                ('category', models.CharField(choices=[('', 'Category'), ('Homes', (('house', 'House'), ('flat', 'Flat'), ('up', 'Upper Portion'), ('lp', 'Lower Portion'), ('fh', 'Farm House'), ('room', 'Room'), ('ph', 'Penthouse'))), ('Plots', (('rp', 'Residential Plots'), ('cp', 'Commercial Plots'), ('al', 'Agricultural Land'), ('il', 'Industrial Land'), ('pfile', 'Plot File'), ('pform', 'Plot Form'))), ('Commercial', (('off', 'Office'), ('shop', 'Shop'), ('wh', 'Warehouse'), ('fact', 'Factory'), ('buil', 'Building'))), ('other', 'Other')], default='', max_length=5)),
                ('bedroom', models.CharField(blank=True, choices=[('S', 'Studio'), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10)], max_length=6, null=True)),
                ('custom_bedroom', models.CharField(blank=True, max_length=3, null=True)),
                ('bathroom', models.CharField(blank=True, choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6)], max_length=1, null=True)),
                ('custom_bathroom', models.CharField(blank=True, max_length=3, null=True)),
                ('area_size', models.IntegerField()),
                ('area_size_unit', models.CharField(choices=[('SFt', 'Sq. Ft.'), ('SM', 'Sq. M.'), ('SYd', 'Sq. Yd.'), ('M', 'Marla'), ('K', 'Kanal')], default='M', max_length=10)),
                ('city', models.CharField(choices=[('', 'City'), ('abd', 'Attock'), ('abt', 'Abbottabad'), ('bhr', 'Bahawalnagar'), ('bwn', 'Bhawana'), ('bhk', 'Bhakkar'), ('bwp', 'Bahawalpur'), ('cwp', 'Chishtian'), ('dgh', 'Dera Ghazi Khan'), ('dnb', 'Dinawali'), ('dip', 'Dipalpur'), ('fdr', 'Fateh Jhang'), ('fsl', 'Faisalabad'), ('ghk', 'Gujar Khan'), ('gjr', 'Gujranwala'), ('grk', 'Gwadar'), ('grw', 'Gujranwala'), ('gjr', 'Gujrat'), ('hyd', 'Hyderabad'), ('isl', 'Islamabad'), ('jlm', 'Jalalpur'), ('jwn', 'Jaranwala'), ('jwp', 'Jhelum'), ('khr', 'Khairpur'), ('khi', 'Karachi'), ('khr', 'Khanewal'), ('ktt', 'Kotli'), ('kwb', 'Kot Adu'), ('lai', 'Lalamusa'), ('lhr', 'Lahore'), ('ldr', 'Lodhran'), ('lrd', 'Larkana'), ('ltr', 'Layyah'), ('mll', 'Mian Channu'), ('mlk', 'Malakwal'), ('mlt', 'Mardan'), ('mrd', 'Multan'), ('mnt', 'Mansehra'), ('mgw', 'Mandi Bahauddin'), ('mwm', 'Mianwali'), ('mtr', 'Multan'), ('mzt', 'Murree'), ('mzw', 'Muzaffargarh'), ('ngt', 'Narowal'), ('nwn', 'Nankana Sahib'), ('pwp', 'Peshawar'), ('phl', 'Pattoki'), ('qta', 'Quetta'), ('qrb', 'Quetta Residency'), ('rch', 'Rajanpur'), ('rnw', 'Rawalpindi'), ('rkn', 'Rahim Yar Khan'), ('rwp', 'Rawalpindi'), ('sgr', 'Sargodha'), ('skt', 'Sialkot'), ('shw', 'Sheikhupura'), ('swn', 'Swat'), ('sak', 'Sargodha'), ('sbq', 'Sahiwal'), ('ska', 'Sakrand'), ('skz', 'Sukheki'), ('stw', 'Sialkot'), ('suk', 'Sukkur'), ('swl', 'Sahiwal'), ('sgr', 'Sargodha'), ('swl', 'Sialkot'), ('saw', 'Sawat'), ('ttn', 'Toba Tek Singh'), ('vhn', 'Vehari'), ('wah', 'Wah Cantt'), ('wln', 'Wazirabad')], default='lhr', max_length=3)),
                ('address', models.TextField(max_length=250)),
                ('description', models.TextField(max_length=700)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, help_text='Change Listing Visibility', verbose_name='Listing Visibility')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing', to=settings.AUTH_USER_MODEL)),
                ('user_wishlist', models.ManyToManyField(blank=True, related_name='user_wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated',),
            },
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to=listing.models.ListingImage.user_directory_path)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='img', to='listing.listing')),
            ],
        ),
    ]