from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Listing, ListingImage, Category


class listingForm (ModelForm):
	custom_bedroom = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Custom Bedrooms',
		'aria-label': 'bed'
	}), required=False, label=_("Bedroom"))
	custom_bathroom = forms.IntegerField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Custom Baths',
		'aria-label': 'baths'
	}), required=False, label=_("Bathroom"))
	custom_floor = forms.IntegerField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Custom Floor level',
		'aria-label': 'floors'
	}), required=False, label=_("Floor Level"))
	area_size = forms.IntegerField(widget=forms.NumberInput(attrs={
		'class': 'form-control mt-2',
		'placeholder': 'Enter area size',
		'aria-label': 'area size'
	}))
	purpose = forms.CharField(widget=forms.TextInput(attrs={
		'hidden': True,
		'aria-label': 'purpose'
	}), required=False)
	furnished = forms.CharField(widget=forms.TextInput(attrs={
		'hidden': True,
		'aria-label': 'furnished'
	}), required=False)
	state = forms.CharField(widget=forms.TextInput(attrs={
		'hidden': True,
		'aria-label': 'construction state'
	}), required=False)
	class Meta:
		model = Listing

		exclude = ('creator', 'time_created', 'is_active', 'user_wishlist', 'is_sold')

		labels = {
			'title': 'Property Title',
			'area_size_unit': 'Area Size Unit',
		}

		widgets = {
            'address': forms.TextInput(),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name in self.fields:
			self.fields[field_name].widget.attrs.update({
				'class': 'form-control mt-2',
				'placeholder': field_name.replace('_', ' ').title()
			})
		self.fields['description'].widget.attrs.update({
			'rows': 3,
			'placeholder': 'Write a brief description about your property ...'
		})
		self.fields['city'].widget.attrs.update({
			'class': 'form-select mt-2',
		})
		self.fields['price'].widget.attrs.update({
			'min': 0,
			'placeholder': 'Enter Price'
		})
		self.fields['area_size_unit'].widget.attrs.update({
			'class': 'form-select mt-2',
		})
		self.fields['category'].widget.attrs.update({
			'class': 'form-select',
			'hidden': True
		})


class listingGetRequestForm (forms.Form):
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
	AREA_SIZE_CHOICES = (
		('', 'Unit'),
		('SFt', 'Sq. Ft.'),
		('SM', 'Sq. M.'),
		('SYd', 'Sq. Yd.'),
		('M', 'Marla'),
		('K', 'Kanal'),
	)

	class CategoryChoiceField(forms.ModelChoiceField):
		def label_from_instance(self, obj):
			# This function will generate the display label for each category.
			# It adds appropriate indentation using dashes ('---') to represent the hierarchy.
			return '---' * obj.get_level() + str(obj)

	city = forms.CharField(widget=forms.Select(attrs={
		'class': 'form-select',
		'title': 'Select City',
	}, choices=CITY_CHOICES), required=False)
	category_query = CategoryChoiceField(
        queryset=Category.objects.all(),
        empty_label="Category",  # Optional, set a custom label for the empty option
        widget=forms.Select(attrs={'class': 'form-select'}),
		required=False
    )
	location = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Search by Location',
	}), label='', required=False)
	min_price = forms.CharField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Min Price',
		'min': 10000,
	}), label='', required=False, min_length=4)
	max_price = forms.CharField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Max Price',
		'min': 10000,
	}), label='', required=False, min_length=4)
	area_size = forms.CharField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Area Size',
		'min': 0
	}), label='', required=False)
	area_size_unit = forms.CharField(widget=forms.Select(attrs={
		'class': 'form-select',
		'title': 'Select Unit',
	}, choices=AREA_SIZE_CHOICES), required=False)
