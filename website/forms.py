from django import forms
from django.forms import ModelForm

from .models import listing, Comments, Images


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
			'description': 'Property Description',
			'area_size': 'Area Size',
			'area_size_unit': 'Area Unit',
		}

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
			'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price', 'min': 0}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
			'purpose': forms.RadioSelect(attrs={'class': 'form-radio-inline'}),
			'area_size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Area Size', 'min': 0}),
            'area_size_unit': forms.Select(attrs={'class': 'form-select'}),
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
