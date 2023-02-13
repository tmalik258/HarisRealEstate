from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	# path('contact_message', views.contact, name = 'contact'),
	path('properties', views.properties, name = 'properties'),
	path('properties/<str:category>', views.properties_category, name = 'properties_category'),
	path('properties/property/<str:item>', views.single_property, name = 'single_property'),
	path('about_us', views.about_us, name = 'about_us'),
	path('agents', views.agents, name = 'agents'),
	path('contact_us', views.contact_us_page, name = 'contact_us_page'),
	path('contact', views.contact, name = 'contact_us'),
	path('createListing', views.createListing, name = 'createListing'),
	path('profile', views.profile, name = 'profile'),
	path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]