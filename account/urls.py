from django.urls import path
from django.contrib.auth.views import (LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView)
from django.views.generic import TemplateView

from . import views
from .forms import (LoginForm, PwdResetForm, PwdResetConfirmForm)

app_name = 'account'

urlpatterns = [
	# login
	path("login", views.CustomLoginView.as_view(
		template_name='account/user/login.html', 
		form_class=LoginForm
	), name="login"),
	# logout
	path("logout", views.logout_view, name="logout"),
	# register
	path('register/', views.register, name='register'),
	# account activation
	path('activate/<slug:uid64>/<slug:token>/', views.account_activate, name='activate'),
	# password reset
	path('password_reset', PasswordResetView.as_view(
		template_name='account/pwd_reset/password_reset.html',
		success_url='password_reset/password_reset_email_confirm/',
		email_template_name='account/pwd_reset/password_reset_email.html',
		form_class=PwdResetForm
		), name='pwd_reset'),
	# password reset email confirm
	path('password_reset/password_reset_email_confirm/', views.CustomLoginView.as_view(
		template_name='account/user/login.html', 
		form_class=LoginForm
		), name='password_reset_done'),
	# password reset confirm
	path('password_reset_confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(
		template_name='account/pwd_reset/password_reset_confirm.html',
		success_url='password_reset_complete/',
		form_class=PwdResetConfirmForm
		), name='pwd_reset_confirm'),
	# password reset complete
	path('password_reset_confirm/<slug:token>/set-password/password_reset_complete/', views.CustomLoginView.as_view(
		template_name='account/user/login.html', 
		form_class=LoginForm
		), name='password_reset_complete'),

	# user dashboard
	# profile delete
	path('profile/delete/user/', views.delete_user, name='delete_user'),
	# profile delete confirmation
	path('profile/delete_confirm/', TemplateView.as_view(template_name='account/user/delete_confirm.html'), name='delete_confirm'),
	# wishlist
	path('wishlist/', views.WishlistView.as_view(), name="wishlist"),
	path('wishlist/add_to_wishlist/<uuid:item>', views.Add_to_wishlist_view, name="add-to-wishlist"),
	# profile
	path('profile', views.profileWithPropertiesListView.as_view(), name='profile'),
	# User Ads
	path('listings', views.userPropertiesListView.as_view(), name='user-listings'),
	# profile update
	path('profile-update', views.profileUpdate, name='profile-update'),
	# profile image update
	path('profile-image-update', views.profileImageUpdate, name='profile-image-update'),
	# password changer form
	path('change-password', PasswordChangeView.as_view(
		template_name='account/user/update_password.html',
		success_url='/account/profile'
	), name='change-password'),
]