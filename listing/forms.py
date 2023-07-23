from django import forms
from django.forms import ModelForm

from .models import Listing, ListingImage, Category


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

		exclude = ('creator', 'time_created', 'is_active', 'user_wishlist', 'is_sold')

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
	category = CategoryChoiceField(
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
