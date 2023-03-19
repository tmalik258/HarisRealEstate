from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import listing, Comments, Images, Contact, Profile

# Register your models here.


# User Model
class UserProfileInline (admin.TabularInline):
	model = Profile
	fk_name = 'user'
	max_num = 1
	can_delete = False
	verbose_name_plural = _('profile')



class UserAdmin (UserAdmin):
	inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)


# Listing Model
class ListingAdmin (admin.ModelAdmin):
	list_display = ('title', 'purpose', 'category', 'bedroom', 'bathroom', 'area_size', 'area_size_unit', 'active', 'creator', 'time_created')
	list_filter = ('purpose', 'category', 'bedroom', 'bathroom', 'area_size', 'area_size_unit', 'active', 'creator', 'time_created')

	# def get_images (self, obj):
	# 	return obj.img
	# get_images.short_description = 'Images'
	# get_images.admin_order_field = 'img__images'
	# get_images.empty_value_display = 'Empty'

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