from django import forms
from django.forms import ModelForm
from .models import listing, Comments, Images, Contact

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

class contactForm (ModelForm):
	class Meta:
		model = Contact
		fields = ('__all__')

		exclude = ('time_created',)

		labels = {
			'fname': '*First Name',
			'lname': 'Last Name',
			'email': '*Email',
			'message': '*Message',
		}

		widgets = {
			'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your First Name?', 'id': 'first_name'}),
			'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your Last Name?', 'id': 'last_name'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'What is your Email? i.e., name@example.com', 'id': 'email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Your Message', 'id': 'message'}),
		}