from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages

from .models import listing, User, Comments, Images, Contact

# Register your models here.


# Admin Site Customization
# class MyAdminSite (admin.AdminSite):
# 	# Text to put at the end of each page's <title>.
#     site_title = ugettext_lazy('My site admin')

#     # Text to put in each page's <h1> (and above login form).
#     site_header = ugettext_lazy('Haris Real Estate administration')

#     # Text to put at the top of the admin index page.
#     index_title = ugettext_lazy('Site administration | Haris Real Estate Site Administration')
# admin_site = MyAdminSite()


# User Model
admin.site.register(User, UserAdmin)

# Listing Model
class ListingAdmin (admin.ModelAdmin):
	list_display = ('title', 'purpose', 'category', 'bedroom', 'bathroom', 'area_size', 'area_size_unit', 'active', 'creator', 'time_created')

	@admin.action
	def make_active (self, request, queryset):
		queryset.update(active=True)
		messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

	@admin.action
	def make_inactive (self, request, queryset):
		queryset.update(active=False)
		messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")

	actions = ['make_active', 'make_inactive']

admin.site.register(listing, ListingAdmin)

# Contact Model
admin.site.register(Contact)

# Comment Model
admin.site.register(Comments)

# Image Model
class ImageAdmin (admin.ModelAdmin):
	list_display = ('listing', 'image_tag')
admin.site.register(Images, ImageAdmin)