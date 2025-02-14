from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (AuthenticationForm, SetPasswordForm, PasswordResetForm)

from .models import User, Profile


class LoginForm(AuthenticationForm):

	username = forms.CharField(widget=forms.TextInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Email or Username',
			'autofocus': 'autofocus'
		}
	))
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Password',
		}
	))

	def clean(self):
		cleaned_data = super().clean()
		username_or_email = cleaned_data.get('username')
		password = cleaned_data.get('password')

		if username_or_email and password:
			# Try to authenticate using username
			user = authenticate(username=username_or_email, password=password)
			
			# If authentication fails, check if it's an email and try again
			if user is None and '@' in username_or_email:
				from django.contrib.auth import get_user_model
				User = get_user_model()
				
				try:
					user_obj = User.objects.get(email=username_or_email)
					user = authenticate(username=user_obj.username, password=password)
				except User.DoesNotExist:
					pass

			if user is None:
				raise forms.ValidationError("Invalid username/email or password.")
		
		return cleaned_data


class RegistrationUserForm(forms.ModelForm):
	username = forms.CharField(label='Username', min_length=4, max_length=50, help_text='Required')
	email = forms.EmailField(max_length=100, help_text='Required', error_messages={'required': 'Sorry, you will need an email address'})
	password = forms.CharField(label='Password', widget=forms.PasswordInput(), help_text='Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.')
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')


	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		r = User.objects.filter(username=username)
		if r.count():
			raise forms.ValidationError('Username already exists')
		return username

	def cleaned_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Passwords do not match.')
		return cd['password2']

	def cleaned_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError(
				'Please use another email, this is already taken or used.'
			)
		return email

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# first_name field
		self.fields['first_name'].widget.attrs.update({
			'placeholder': 'First Name',
			'class': 'form-control',
			'autofocus': 'autofocus'
		})
		self.fields['first_name'].help_text = 'Required'

		# last_name field
		self.fields['last_name'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Last Name'
		})
		self.fields['last_name'].help_text = 'Required'

		# username field
		self.fields['username'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Username',
		})

		# email field
		self.fields['email'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Email',
			'name': 'email'
		})

		# password field
		self.fields['password'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Password'
		})

		# password2 field
		self.fields['password2'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Repeat Password'
		})


class RegisterationProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('__all__')
		exclude = ('user',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name in self.fields:
			self.fields[field_name].widget.attrs.update({
				'class': 'form-control',
				'placeholder': field_name.replace('_', ' ').title()
			})
		self.fields['bio_info'].widget.attrs.update({
			'rows': 3,
			'placeholder': 'Write about yourself or your agency ...'
		})


class PwdResetForm(PasswordResetForm):
	email = forms.EmailField(max_length=254, widget=forms.EmailInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Email',
			'autofocus': 'autofocus'
		}
	))

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			user = User.objects.get(email=email)
		except ObjectDoesNotExist:
			raise forms.ValidationError(
				'Unfortunately we can not find that email address.'
			)
		return email


class PwdResetConfirmForm(SetPasswordForm):
	new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Enter New Password',
			'autofocus': 'autofocus'
		}
	))
	new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'Enter Repeat Password',
		}
	))


# Create a UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']

		widgets = {
			'username': forms.TextInput(attrs={
				'placeholder': 'Username',
				'class': 'form-control'
			}),
			'first_name': forms.TextInput(attrs={
				'placeholder': 'First Name',
				'class': 'form-control'
			}),
			'last_name': forms.TextInput(attrs={
				'placeholder': 'Last Name',
				'class': 'form-control'
			}),
			'email': forms.EmailInput(attrs={
				'placeholder': 'Your Email',
				'class': 'form-control'
			}),
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
			'readonly': True
		})
