from django import forms
from django.forms import ModelForm

from .models import Listing, ListingImage


class listingForm (ModelForm):
	custom_bedroom = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Custom Bedrooms'
	}), required=False)
	custom_bathroom = forms.IntegerField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Custom Baths'
	}), required=False)
	custom_floor = forms.IntegerField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Custom Floor level',
	}), required=False)
	area_size = forms.IntegerField(widget=forms.NumberInput(attrs={
		'class': 'form-control mt-2',
		'placeholder': 'Enter area size'
	}))
	purpose = forms.CharField(widget=forms.TextInput(attrs={
		'hidden': True
	}), required=False)
	furnished = forms.CharField(widget=forms.TextInput(attrs={
		'hidden': True
	}), required=False)
	state = forms.CharField(widget=forms.TextInput(attrs={
		'hidden': True
	}), required=False)
	class Meta:
		model = Listing
		fields = ('__all__')

		exclude = ('creator', 'time_created', 'is_active', 'user_wishlist', 'is_sold', 'bedroom', 'bathroom')

		labels = {
			'title': 'Property Title',
			'price': 'Price',
			'address': 'Address',
			'description': 'Description',
			'area_size_unit': 'Area Unit',
		}

		widgets = {
			'title': forms.TextInput(attrs={
				'class': 'form-control mt-2',
				'placeholder': 'Title',
			}),
			'price': forms.NumberInput(attrs={
				'class': 'form-control mt-2',
				'id': 'price_input',
				'placeholder': 'Enter Price',
				'min': 0
			}),
            'category': forms.Select(attrs={
				'class': 'form-select mt-2',
				'hidden': True,
				# 'id': 'id_category'
			}),
            'city': forms.Select(attrs={
				'class': 'form-select mt-2',
			}),
            'address': forms.TextInput(attrs={
				'class': 'form-control mt-2',
				'placeholder': 'Address',
			}),
            'description': forms.Textarea(attrs={
				'class': 'form-control mt-2',
				'placeholder': 'Write a description about your property',
			}),
            'area_size_unit': forms.Select(attrs={
				'class': 'form-select mt-2',
				'id': 'area_size_unit'
			}),
		}
	
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['purpose'].widget.attrs.update({
	# 		'hidden': True
	# 	})


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
	('any', 'Any'),
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

class listingGetRequestForm (ModelForm):
	city = forms.CharField(widget=forms.Select(attrs={
		'class': 'form-select',
		'title': 'Select City',
		'id': ''
	}, choices=CITY_CHOICES), required=False)
	category = forms.CharField(widget=forms.Select(attrs={
		'class': 'form-select',
		'title': 'Select Category',
		'id': ''
	}, choices=CATEGORY_CHOICES))
	location = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Search by Location',
		'id': ''
	}), label='', required=False)
	min_price = forms.CharField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Min Price',
		'min': 10000,
		'id': ''
	}), label='', required=False, min_length=4)
	max_price = forms.CharField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Max Price',
		'min': 10000,
		'id': ''
	}), label='', required=False, min_length=4)
	area_size = forms.CharField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Area Size',
		'id': '',
		'min': 0
	}), label='', required=False)

	class Meta:
		model = Listing
		fields = ('__all__')

		exclude = ('creator', 'time_created','active', 'title', 'description', 'address', 'price', 'purpose', 'city')

		labels = {
			# 'price': 'Price',
			'category': '',
			'address': '',
			'area_size': ''
		}

		widgets = {
				'title': 'Select Category',
			# 'purpose': forms.Select(attrs={
			# 	'class': 'form-select',
			# 	'required': 'false',
			# 	'title': 'Option for Sale or Rent'
			# }),
			# 'area_size': forms.NumberInput(attrs={
			# 	'class': 'form-control',
			# 	'min': 0,
			# 	'placeholder': 'Area Size'
			# }, required=False),
			# 'city': forms.Select(attrs={
			# 	'class': 'form-select',
			# 	'title': 'Select City'
			# }),
			'area_size_unit': forms.Select(attrs={
				'class': 'form-select',
				'title': 'Specify Unit for Area Size',
				'id': ''
			}),
		}