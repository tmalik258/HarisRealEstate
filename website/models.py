from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

# Create your models here.

class User (AbstractUser):
	def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
		return 'images/user_{0}/profile_image/{1}'.format(instance.username, filename)
	bio_info = models.TextField(max_length=500)
	profile_image = models.ImageField(upload_to = user_directory_path, blank=True)
	phone_number = PhoneNumberField(blank=True)

class listing (models.Model):
	PURPOSE_CHOICES = (
		('S', 'Sale'),
		('R', 'Rent Out')
	)
	CITY_CHOICES = (
		('lhr', 'Lahore'),
		('khi', 'Karachi'),
		('isl', 'Islamabad')
	)
	CATEGORY_CHOICES = [
		('Homes', (
			('house', 'House'),
			# ('flat', 'Flat'),
			# ('up', 'Upper Portion'),
			# ('lp', 'Lower Portion'),
			# ('fh', 'Farm House'),
			# ('room', 'Room'),
			# ('ph', 'Penthouse')
		)),
		('Plots', (
			('rp', 'Residential Plots'),
			# ('cp', 'Commercial Plots'),
			# ('al', 'Agricultural Land'),
			# ('il', 'Industrial Land'),
			# ('pfile', 'Plot File'),
			# ('pform', 'Plot Form'),
		)),
		('Commercial', (
			('off', 'Office'),
			# ('shop', 'Shop'),
			# ('wh', 'Warehouse'),
			# ('fact', 'Factory'),
			# ('buil', 'Building'),
		)),
		('other', 'Other')
	]
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listingUser")
	title = models.CharField(max_length=64)
	price = models.IntegerField()
	purpose = models.CharField( max_length=2, choices=PURPOSE_CHOICES, default='S')
	category = models.CharField( max_length=5, choices=CATEGORY_CHOICES, default='')
	area_size = models.IntegerField()
	city = models.CharField( max_length=3, choices=CITY_CHOICES, default='lhr')
	address = models.TextField(max_length=100)
	description = models.TextField(max_length=300)
	time_created = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	def __str__(self) -> str:
		if self.active:
			listing = 'Listing is Active'
		else:
			listing = 'Listing is Closed'
		time = self.time_created.strftime("%H:%M | %d-%m-%Y")
		return f"Listing: {self.id} | {self.title} | ({self.creator}, {time}) | {listing}"

class Comments (models.Model):
	fname = models.CharField(max_length=24)
	lname = models.CharField(max_length=24)
	listing = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="comments")
	comment = models.TextField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		time = self.date_created.strftime("%H:%M | %d-%m-%Y")
		return f"{self.creator} | {self.auction_list.title} | {time}"

class Images (models.Model):
	def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/listing_<title>/<filename>
		return 'images/user_{0}/listing_{1}/{2}'.format(instance.listing.creator.username, instance.listing.title, filename)
	images = models.ImageField(upload_to = user_directory_path, blank=True)
	listing = models.ForeignKey(listing, on_delete= models.CASCADE, related_name='img')

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