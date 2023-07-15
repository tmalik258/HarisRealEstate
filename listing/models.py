import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Image Resize and Upload
from django.utils.crypto import get_random_string
from django.utils import timezone
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image as PillowImage
from django.utils.safestring import mark_safe


# Model Managers
class ListingManager(models.Manager):
	def get_queryset(self):
		return super(ListingManager, self).get_queryset().filter(is_active=True)


# Create your models here.
class Listing (models.Model):
	AREA_SIZE_CHOICES = (
		('SFt', 'Sq. Ft.'),
		('SM', 'Sq. M.'),
		('SYd', 'Sq. Yd.'),
		('M', 'Marla'),
		('K', 'Kanal'),
	)

	PURPOSE_CHOICES = (
		('S', 'For Sale'),
		('R', 'For Rent')
	)

	BEDROOM_CHOICES = (
		('S', 'Studio'),
		('1', 1),
		('2', 2),
		('3', 3),
		('4', 4),
		('5', 5),
		('6', 6),
		('7', 7),
		('8', 8),
		('9', 9),
		('10', 10)
	)

	BATHROOM_CHOICES = (
		('1', 1),
		('2', 2),
		('3', 3),
		('4', 4),
		('5', 5),
		('6', 6)
	)

	CITY_CHOICES = (
		('', 'City'),
		('abd', 'Attock'),
		('abt', 'Abbottabad'),
		('bhr', 'Bahawalnagar'),
		('bwn', 'Bhawana'),
		('bhk', 'Bhakkar'),
		('bwp', 'Bahawalpur'),
		('cwp', 'Chishtian'),
		('dgh', 'Dera Ghazi Khan'),
		('dnb', 'Dinawali'),
		('dip', 'Dipalpur'),
		('fdr', 'Fateh Jhang'),
		('fsl', 'Faisalabad'),
		('ghk', 'Gujar Khan'),
		('gjr', 'Gujranwala'),
		('grk', 'Gwadar'),
		('grw', 'Gujranwala'),
		('gjr', 'Gujrat'),
		('hyd', 'Hyderabad'),
		('isl', 'Islamabad'),
		('jlm', 'Jalalpur'),
		('jwn', 'Jaranwala'),
		('jwp', 'Jhelum'),
		('khr', 'Khairpur'),
		('khi', 'Karachi'),
		('khr', 'Khanewal'),
		('ktt', 'Kotli'),
		('kwb', 'Kot Adu'),
		('lai', 'Lalamusa'),
		('lhr', 'Lahore'),
		('ldr', 'Lodhran'),
		('lrd', 'Larkana'),
		('ltr', 'Layyah'),
		('mll', 'Mian Channu'),
		('mlk', 'Malakwal'),
		('mlt', 'Mardan'),
		('mrd', 'Multan'),
		('mnt', 'Mansehra'),
		('mgw', 'Mandi Bahauddin'),
		('mwm', 'Mianwali'),
		('mtr', 'Multan'),
		('mzt', 'Murree'),
		('mzw', 'Muzaffargarh'),
		('ngt', 'Narowal'),
		('nwn', 'Nankana Sahib'),
		('pwp', 'Peshawar'),
		('phl', 'Pattoki'),
		('qta', 'Quetta'),
		('qrb', 'Quetta Residency'),
		('rch', 'Rajanpur'),
		('rnw', 'Rawalpindi'),
		('rkn', 'Rahim Yar Khan'),
		('rwp', 'Rawalpindi'),
		('sgr', 'Sargodha'),
		('skt', 'Sialkot'),
		('shw', 'Sheikhupura'),
		('swn', 'Swat'),
		('sak', 'Sargodha'),
		('sbq', 'Sahiwal'),
		('ska', 'Sakrand'),
		('skz', 'Sukheki'),
		('stw', 'Sialkot'),
		('suk', 'Sukkur'),
		('swl', 'Sahiwal'),
		('sgr', 'Sargodha'),
		('swl', 'Sialkot'),
		('saw', 'Sawat'),
		('ttn', 'Toba Tek Singh'),
		('vhn', 'Vehari'),
		('wah', 'Wah Cantt'),
		('wln', 'Wazirabad'),
	)

	CATEGORY_CHOICES = [
		('', 'Category'),
		('Homes', (
			('house', 'House'),
			('flat', 'Flat'),
			('up', 'Upper Portion'),
			('lp', 'Lower Portion'),
			('fh', 'Farm House'),
			('room', 'Room'),
			('ph', 'Penthouse')
		)),
		('Plots', (
			('rp', 'Residential Plots'),
			('cp', 'Commercial Plots'),
			('al', 'Agricultural Land'),
			('il', 'Industrial Land'),
			('pfile', 'Plot File'),
			('pform', 'Plot Form'),
		)),
		('Commercial', (
			('off', 'Office'),
			('shop', 'Shop'),
			('wh', 'Warehouse'),
			('fact', 'Factory'),
			('buil', 'Building'),
		)),
		('other', 'Other')
	]

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listing")
	title = models.CharField(max_length=64)
	price = models.IntegerField()
	purpose = models.CharField( max_length=2, choices=PURPOSE_CHOICES, default='S')
	category = models.CharField( max_length=5, choices=CATEGORY_CHOICES, default='')
	bedroom = models.CharField(max_length=6, choices=BEDROOM_CHOICES, null=True, blank=True)
	custom_bedroom = models.CharField(max_length=3, null=True, blank=True)
	bathroom = models.CharField(max_length=1, choices=BATHROOM_CHOICES, null=True, blank=True)
	custom_bathroom = models.CharField(max_length=3, null=True, blank=True)
	area_size = models.IntegerField()
	area_size_unit =  models.CharField( max_length=10, choices=AREA_SIZE_CHOICES, default='M')
	city = models.CharField( max_length=3, choices=CITY_CHOICES, default='lhr')
	address = models.TextField(max_length=250)
	description = models.TextField(max_length=700)
	user_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_wishlist', blank=True)
	time_created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(verbose_name=_("Listing Visibility"), help_text=_("Change Listing Visibility"), default=True)
	objects = models.Manager()
	posts = ListingManager()

	class Meta:
		ordering = (('-updated'),)

	def get_bedroom(self):
		if self.custom_bedroom:
			return self.custom_bedroom
		elif self.bedroom:
			if self.bedroom == 'S':
				return 'Studio'
			else:
				return self.bedroom
		else:
			return False

	def get_bathroom(self):
		if self.custom_bathroom:
			return self.custom_bathroom
		elif self.bathroom:
			return self.bathroom
		else:
			return False

	def __str__(self) -> str:
		if self.is_active:
			active = 'Active'
		else:
			active = 'InActive'
		time = self.time_created.strftime("%H:%M | %d-%m-%Y")
		return f"{self.title} | ({self.creator}, {time}) | {active}"


# class Comment (models.Model):
# 	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
# 	comment = models.TextField(max_length=255)
# 	date_created = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		time = self.date_created.strftime("%H:%M | %d-%m-%Y")
# 		return f"{self.creator} | {self.auction_list.title} | {time}"


class ListingImage (models.Model):
	def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/listing_<title>/<filename>
		return 'user_{0}/listing_{1}/{2}'.format(instance.listing.creator.username, instance.listing.title, filename)
	image = models.ImageField(upload_to = user_directory_path)
	listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name='img')

	def __str__(self):
		return f"{self.listing.title}"

	def save(self, *args, **kwargs):
		print(f"In save function: {self.image}")
		img = PillowImage.open(self.image)
		# Resize image
		output_size = (500, 500)
		img.thumbnail(output_size)

		# Save the resized image to a BytesIO buffer
		output_buffer = BytesIO()
		img.save(output_buffer, format='WebP')
		output_buffer.seek(0)

		# Generate a unique name for the image
		random_string = get_random_string(length=8)
		timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
		filename = f'{random_string}_{timestamp}.webp'

		# Save the buffer content to the image field with the unique filename
		self.image.save(filename, ContentFile(output_buffer.read()), save=False)

		# Save the buffer content to the image field
		# self.image.save(self.image.name, ContentFile(output_buffer.read()), save=False)
		print(f"In save function2: {self.image.name}")
		super().save(*args, **kwargs)
	
	def image_tag(self):
		return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)

	image_tag.short_description = 'Image'


class Contact (models.Model):
	fname = models.CharField(max_length=24)
	lname = models.CharField(max_length=24, blank=True)
	phone_number = PhoneNumberField()
	email = models.EmailField(max_length=254)
	message = models.TextField(max_length=500)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		time = self.date_created.strftime("%H:%M | %d-%m-%Y")
		return f"{self.fname} | {self.email} | {time}"
