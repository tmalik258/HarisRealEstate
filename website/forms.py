from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import listing, Comments, Images, Profile


# Create a UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# Create a ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('__all__')
		exclude = ('user',)


class listingForm (ModelForm):
	class Meta:
		model = listing
		fields = ('__all__')

		exclude = ('creator', 'time_created','active')

		labels = {
			'title': 'Property Title',
			'price': 'Price',
			'category': 'Category',
			'address': 'Address',
			'description': 'Description',
			'area_size': 'Area Size',
			'area_size_unit': 'Area Unit',
		}

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
			'price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'price_input', 'placeholder': 'Enter Price', 'min': 0}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'category_input'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description about your property'}),
			'purpose': forms.RadioSelect(attrs={'class': 'form-radio-inline'}),
			'bedroom': forms.RadioSelect(attrs={'id': 'bedroom_input'}),
			'bathroom': forms.RadioSelect(attrs={'id': 'bathroom_input'}),
			'area_size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Area Size', 'min': 0}),
            'area_size_unit': forms.Select(attrs={'class': 'form-select'}),
		}


CITY_CHOICES = (
		('', 'Choose City'),
		('lhr', 'Lahore'),
		('khi', 'Karachi'),
		('isl', 'Islamabad')
	)


class listingGetRequestForm (ModelForm):
	city = forms.CharField(widget=forms.Select(attrs={
		'class': 'form-select',
		'title': 'Select Category'
	}, choices=CITY_CHOICES), required=False)
	location = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Search by Location',
		# 'title': 'Temporarily Disabled'
	}), label='', required=False)
	min_price = forms.CharField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Enter Min Price',
		'min': 10000,
		# 'title': 'Temporarily Disabled'
	}), label='', required=False, min_length=4)
	max_price = forms.CharField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Enter Max Price',
		'min': 10000,
		# 'title': 'Temporarily Disabled'
	}), label='', required=False, min_length=4)
	area_size = forms.CharField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'placeholder': 'Area Size',
		# 'title': 'Temporarily Disabled',
		'min': 0
	}), label='', required=False)

	class Meta:
		model = listing
		fields = ('__all__')

		exclude = ('creator', 'time_created','active', 'title', 'description', 'address', 'price', 'purpose', 'city')

		labels = {
			# 'price': 'Price',
			'category': 'Category',
			'address': '',
			'area_size': 'Area Size'
		}

		widgets = {
			# 'price': forms.NumberInput(attrs={
			# 	'class': 'form-control',
			# 	'placeholder': 'Enter Max Price',
			# 	'min': 10000
			# }),
            'category': forms.Select(attrs={
				'class': 'form-select',
				'title': 'Select Category'
			}),
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
			'city': forms.Select(attrs={
				'class': 'form-select',
				'title': 'Select City'
			}),
			'area_size_unit': forms.Select(attrs={
				'class': 'form-select',
				'title': 'Specify Unit for Area Size'
			}),
		}


# class listingFullForm (listingForm):
# 	images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


# 	class Meta (listingForm.Meta):
# 		fields = listingForm.Meta.fields + str('images')

# class imageForm (ModelForm):
# 	class Meta:
# 		model = Images
# 		fields = ('__all__')

# 		exclude = ('listing',)

# 		labels = {
# 			'images': 'Image'
# 		}

# 		widgets = {
# 			'images': forms.ClearableFileInput(attrs={'multiple': True})
# 		}
