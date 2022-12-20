from django import forms
from django.forms import ModelForm
from .models import listing, Comments, Images

class listingForm (ModelForm):
	class Meta:
		model = listing
		fields = ('__all__')

		exclude = ('creator', 'time_created','active')

		labels = {
			'title': 'Title',
			'price': 'Price',
			'category': 'Category',
			'address': 'Address',
			'description': 'Description',
		}

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
			'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price'}),
            'category': forms.Select(attrs={'class': 'custom-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
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