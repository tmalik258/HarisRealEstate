from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'listing'

urlpatterns = [
	# home url
	path('', views.index, name='index'),
	# properties url
	path('properties', views.PropertiesListView.as_view(), name='properties'),
	# single property url
	path('properties/property/<uuid:item>', views.property_detail, name='property-detail'),
	# searched properties display
    path('filtered_properties?', views.SearchedPropertiesListView.as_view(), name='get_property_by_search'),
	# filtered properties display
    path('filtered_properties', views.FilteredPropertiesListView.as_view(), name='get_property'),
	# filtered properties display
    path('properties?category=<str:type>', views.CategoryListView.as_view(), name='get_category'),
	# about us url
	path('about_us', views.about_us, name='about_us'),
	# agents url
	path('agents', views.agents, name='agents'),
	# contact us url
	path('contact_us', views.contact_us_page, name='contact_us_page'),
	# contact us submission view
	path('contact', views.contact, name='contact_us'),
	# create listing url
	path('createListing', views.createListing, name='createListing'),
	# # update listing url
	path('properties/property/<uuid:item_id>/edit', views.updateListing, name='update-listing'),
	# delete listing url
	path('delete-listing/<uuid:item_id>', views.deleteListing, name='delete-listing'),
	# privacy policy url
    path("privacy-policy", views.privacyPolicy, name="privacy-policy"),
	# terms of use url
    path("terms-of-use", views.termsView, name="terms"),
]