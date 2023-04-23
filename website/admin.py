from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Listing, Comment, Image, Contact, Profile

# Register your models here.


# User Model
class UserProfileInline (admin.StackedInline):
	model = Profile
	fk_name = 'user'
	max_num = 1
	can_delete = False
	verbose_name_plural = _('profile')


class UserAdmin (UserAdmin):
	inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)


class ImageInline (admin.TabularInline):
	model = Image
	fk_name = 'listing'
	verbose_name_plural = _('image')


# Listing Model
class ListingAdmin (admin.ModelAdmin):
	inlines = [ImageInline]
	list_display = ('title', 'purpose', 'category', 'bedroom', 'bathroom', 'area_size', 'area_size_unit', 'active', 'creator', 'time_created')
	list_filter = ('purpose', 'category', 'bedroom', 'bathroom', 'area_size', 'area_size_unit', 'active', 'creator', 'time_created')
	empty_value_display = '-empty-'

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs

		return Listing.objects.filter(creator=request.user) or qs.none()
	
	@admin.action
	def make_active (self, request, queryset):
		queryset.update(active=True)
		messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

	@admin.action
	def make_inactive (self, request, queryset):
		queryset.update(active=False)
		messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")

	actions = ['make_active', 'make_inactive']
admin.site.register(Listing, ListingAdmin)


# Contact Model
admin.site.register(Contact)


# Comment Model
admin.site.register(Comment)


# # Image Model
# class ImageAdmin (admin.ModelAdmin):
# 	list_display = ('listing', 'image_tag')

# 	def get_queryset(self, request):
# 		qs = super().get_queryset(request)
# 		if request.user.is_superuser:
# 			return qs

# 		return Image.objects.filter(created_by=request.user) or qs.none()

# admin.site.register(Image, ImageAdmin)