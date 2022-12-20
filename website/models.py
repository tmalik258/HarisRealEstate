from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User (AbstractUser):
	def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
		return 'images/user_{0}/profile_image/{1}'.format(instance.username, filename)
	bio_info = models.TextField(max_length=500)
	profile_image = models.ImageField(upload_to = user_directory_path, blank=True)

class Category (models.Model):
	code = models.CharField(primary_key=True, max_length=24)
	category = models.CharField(max_length=24)
	def __str__(self):
		return f"{self.category}"

class listing (models.Model):
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listingUser")
	title = models.CharField(max_length=64)
	price = models.DecimalField(max_digits=15, decimal_places=4)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="cat")
	address = models.TextField(max_length=100)
	description = models.TextField(max_length=255)
	time_created = models.DateTimeField(auto_created=True)
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
		return 'images/user_{0}/listing_{1}/{2}'.format(instance.creator.username, instance.listing.title, filename)
	images = models.ImageField(upload_to = user_directory_path, blank=True)
	listing = models.ForeignKey(listing, on_delete= models.CASCADE, related_name='img')