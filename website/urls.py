from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	# home page
	path('', views.index, name = 'index'),
	# properties page
	path('properties', views.PropertiesListView.as_view(), name = 'properties'),
	# single property url
	path('properties/property/<str:item>', views.single_property, name = 'single_property'),
	# searched properties display
    path('filtered_properties?', views.SearchedPropertiesListView.as_view(), name = 'get_property_by_search'),
	# filtered properties display
    path('filtered_properties', views.FilteredPropertiesListView.as_view(), name = 'get_property'),
	# filtered properties display
    path('properties?category=<str:type>', views.CategoryListView.as_view(), name = 'get_category'),
	# about us page
	path('about_us', views.about_us, name = 'about_us'),
	# agents page
	path('agents', views.agents, name = 'agents'),
	# contact us page
	path('contact_us', views.contact_us_page, name = 'contact_us_page'),
	# contact us submission view
	path('contact', views.contact, name = 'contact_us'),
	# create listing
	path('createListing', views.createListing, name = 'createListing'),
	# profile page
	path('profile', views.profileWithPropertiesListView.as_view(), name='profile'),
	# profile update page
	path('profile-update', views.profileUpdate, name = 'profile-update'),
	# password changer form
	path('change-password', auth_views.PasswordChangeView.as_view(
		template_name='website/change-password.html',
		success_url='/profile'
	), name='change-password'),
	# login page
	path("login", views.login_view, name="login"),
	# logout url
    path("logout", views.logout_view, name="logout"),
	# register page
    path("register", views.register, name="register"),
]