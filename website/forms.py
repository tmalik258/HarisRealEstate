from django import forms
from django.forms import ModelForm
from .models import listing, Comments, Images

class listingForm (ModelForm):
	class Meta:
		PURPOSE_CHOICES = (
			('S', 'Sale'),
			('R', 'Rent Out')
		)
		model = listing
		fields = ('__all__')

		exclude = ('creator', 'time_created','active')

		labels = {
			'title': ' Property Title',
			'price': 'Price',
			'category': 'Category',
			'address': 'Address',
			'description': 'Property Description',
			'area_size': 'Area Size (in marla)'
		}

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
			'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price', 'min': 0}),
            'category': forms.Select(attrs={'class': 'custom-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
			'purpose': forms.RadioSelect(),
			'area_size': forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
		}

class imageForm (ModelForm):
	class Meta:
		model = Images
		fields = ('__all__')

		exclude = ('listing',)

		labels = {
			'images': 'Image'
		}

		widgets = {
			'images': forms.ClearableFileInput()
		}