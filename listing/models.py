import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# external packages
from phonenumber_field.modelfields import PhoneNumberField
from mptt.models import MPTTModel, TreeForeignKey

# Image Resize and Upload
from django.utils.crypto import get_random_string
from django.utils import timezone
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image as PillowImage
from django.utils.safestring import mark_safe


# Create your models here.
class Category (MPTTModel):
	"""
	Category table implimented with MPTT
	"""
	name = models.CharField(
		verbose_name=_("Category Name"),
		help_text=_("Required and unique"),
		max_length=124,
		unique=True
	)
	slug = models.SlugField(verbose_name=_("Category Safe URL"), max_length=255, unique=True)
	parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

	class MPTTMeta:
		order_insertion_by = ["name"]

	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('listing:get_category', kwargs={
			'category_slug': self.slug
		})

	def save (self, *args, **kwargs):
		if self.slug == '':
			value = self.title.replace(" ", "-")
			self.slug = slugify(value, allow_unicode=True)
		super().save(*args, **kwargs)


class Amenities (models.Model):
	feature = models.CharField(
		verbose_name=_("Feature Name"),
		max_length=124,
		unique=True
	)
	icon = models.CharField(verbose_name=_('Feature Icon'), max_length=124, blank=True, null=True)

	class Meta:
		verbose_name = _('Amenity')
		verbose_name_plural = _('Amenities')

	def __str__(self):
		return self.feature


class ListingAmenity (models.Model):
	amenity = models.ForeignKey(Amenities, on_delete=models.CASCADE, related_name='amenity')
	listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='amenity')

	# def __str__(self):
	# 	return self.amenity.feature


class ListingSpecification(models.Model):
	"""
	The Listing Specification Table contains Listing specification of features for the product types
	"""
	name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)
	
	def __str__(self):
		return self.name


class ListingSpecificationValue(models.Model):
	"""
	The Listing Specification Value table holds each of the products individual specification or bespoke features
	"""
	
	listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name=_('specification_value'))
	specification = models.ForeignKey("ListingSpecification", on_delete=models.RESTRICT)
	value = models.CharField(verbose_name=_("value"), max_length=255, help_text=_("Listing Specification Value (maximum of 255 characters)"))

	def __str__(self):
		return self.value
	
	def clean(self):
		super().clean()

		# Check value based on specification
		if self.specification.name == 'Purpose':
			allowed_values = ['Rent', 'Sale']
		elif self.specification.name == 'Furnished':
			allowed_values = ['Furnished', 'Unfurnished']
		elif self.specification.name == 'Construction State':
			allowed_values = ['Grey Structure', 'Finished']
		else:
			return

		if self.value not in allowed_values:
			raise ValidationError(f"The value '{self.value}' is not allowed for the specification '{self.specification.name}'.")

	def save(self, *args, **kwargs):
		self.clean()  # Validate the value before saving
		super().save(*args, **kwargs)


class Listing (models.Model):
	# Model Managers
	class ListingManager(models.Manager):
		def get_queryset(self):
			return super(models.Manager, self).get_queryset().filter(is_active=True)


	AREA_SIZE_CHOICES = (
		('SFt', 'Sq. Ft.'),
		('SM', 'Sq. M.'),
		('SYd', 'Sq. Yd.'),
		('M', 'Marla'),
		('K', 'Kanal'),
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

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listing")
	title = models.CharField(max_length=64)
	price = models.IntegerField()
	category = TreeForeignKey(Category, on_delete=models.CASCADE, related_name='listing', default=29)
	area_size_unit =  models.CharField( max_length=10, choices=AREA_SIZE_CHOICES, default='M')
	city = models.CharField( max_length=3, choices=CITY_CHOICES, default='lhr')
	address = models.TextField(max_length=250)
	description = models.TextField(max_length=1000)
	user_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_wishlist', blank=True)
	time_created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	is_sold = models.BooleanField(help_text=_("(Un)Mark as sold"), default=False)
	is_active = models.BooleanField(verbose_name=_("Listing Visibility"), help_text=_("Change Listing Visibility"), default=True)
	objects = models.Manager()
	posts = ListingManager()

	class Meta:
		ordering = (('-updated'),)

	def get_specification_value(self, specification_name):
		try:
			return self.specification_value.get(specification__name=specification_name).value
		except ListingSpecificationValue.DoesNotExist:
			return None

	def get_purpose(self):
		return self.get_specification_value('Purpose')

	def get_area_size(self):
		return self.get_specification_value('Area Size')

	def get_bedroom(self):
		return self.get_specification_value('Bedroom')

	def get_bathroom(self):
		return self.get_specification_value('Bathroom')

	def get_floor(self):
		return self.get_specification_value('Floors')

	def get_construction_state(self):
		return self.get_specification_value('Construction State')

	def get_furnished(self):
		return self.get_specification_value('Furnished')

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
		img = PillowImage.open(self.image)
		# Resize image
		output_size = (1000, 1000)
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
